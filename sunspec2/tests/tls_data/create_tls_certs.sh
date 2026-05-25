#!/usr/bin/env bash
#
# Generate the full Secure SunSpec Modbus (mbaps) TLS test PKI.
#
# This script (re)generates every certificate needed by the Secure
# SunSpec Modbus conformance tests. The output is organised as:
#
#   ca/                     shared trust anchors (root + intermediate CAs)
#   server/tls1_2|tls1_3/   valid server certificates per TLS version
#   server/invalid/         deliberately invalid server certificates
#   client/tls1_2|tls1_3/   valid client certificates, one per SunSpec role
#   client/invalid/         deliberately invalid client certificates
#   foreign_pki/            an unrelated, untrusted CA (multiple-PKI tests)
#
# All keys are ECDSA on the NIST P-256 curve, which is required for the
# mandatory Secure SunSpec Modbus cipher suites (ECDHE-ECDSA, P-256 -
# SunSpecTCP-17/42/43/44). Client certificates carry the SunSpec role
# extension at OID 1.3.6.1.4.1.50316.802.1, an ASN.1 UTF8String holding
# exactly one role (SunSpecTCP-29/30/31).
#
# Usage:  ./create_tls_certs.sh
#
set -euo pipefail

# Keep Git Bash / MSYS from mangling the openssl "/C=US/..." subjects.
export MSYS_NO_PATHCONV=1
export MSYS2_ARG_CONV_EXCL='*'

cd "$(dirname "$0")"

CURVE="prime256v1"          # NIST P-256
DAYS=3653                   # ~10 years for valid certificates
SUBJ_BASE="/C=US/ST=California/O=SunSpec Alliance/OU=Secure SunSpec Modbus"

# The four mandatory SunSpec roles (SunSpecTCP-22).
ROLES=(ReadOnlySunSpec GridServiceSunSpec NetworkAdministratorSunSpec SuperAdministratorSunSpec)

echo "Generating Secure SunSpec Modbus TLS test PKI (ECDSA P-256)..."

# --- clean previous output -------------------------------------------------
rm -rf ca server client foreign_pki openssl _cadb
mkdir -p openssl ca server/tls1_2 server/tls1_3 server/invalid \
         client/tls1_2 client/tls1_3 client/invalid foreign_pki _cadb/newcerts
: > _cadb/index.txt
echo 1000 > _cadb/serial

# --- extension templates ---------------------------------------------------
cat > openssl/ext_root_ca.cnf <<'EOF'
basicConstraints     = critical, CA:TRUE
keyUsage             = critical, keyCertSign, cRLSign
subjectKeyIdentifier = hash
EOF

cat > openssl/ext_inter_ca.cnf <<'EOF'
basicConstraints       = critical, CA:TRUE, pathlen:0
keyUsage               = critical, keyCertSign, cRLSign
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid:always,issuer
EOF

# Server leaf: serverAuth, SAN for localhost.
cat > openssl/ext_server.cnf <<'EOF'
basicConstraints       = critical, CA:FALSE
keyUsage               = critical, digitalSignature, keyAgreement
extendedKeyUsage       = serverAuth
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
subjectAltName         = DNS:localhost, IP:127.0.0.1
EOF

# Server leaf without a SAN (negative: hostname verification must fail).
cat > openssl/ext_server_no_san.cnf <<'EOF'
basicConstraints       = critical, CA:FALSE
keyUsage               = critical, digitalSignature, keyAgreement
extendedKeyUsage       = serverAuth
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
EOF

# Build a client-leaf extension file for a given role (or no role).
# $1 = output cnf path   $2 = role string ("" => omit the role extension)
# $3 = ASN.1 string type for the role value (default UTF8String)
write_client_ext() {
    local out="$1" role="$2" asn1type="${3:-UTF8String}"
    cat > "$out" <<'EOF'
basicConstraints       = critical, CA:FALSE
keyUsage               = critical, digitalSignature, nonRepudiation, keyAgreement
extendedKeyUsage       = clientAuth
subjectKeyIdentifier   = hash
authorityKeyIdentifier = keyid,issuer
EOF
    if [ -n "$role" ]; then
        # SunSpec role extension (OID 1.3.6.1.4.1.50316.802.1).
        echo "1.3.6.1.4.1.50316.802.1 = ASN1:${asn1type}:${role}" >> "$out"
    fi
}

# --- helpers ---------------------------------------------------------------
new_key() { openssl ecparam -name "$CURVE" -genkey -noout -out "$1"; }

# Turn an extension .cnf file into a list of `openssl req -addext` args.
ext_to_addext() {
    local line
    ADDEXT_ARGS=()
    while IFS= read -r line || [ -n "$line" ]; do
        [ -z "${line// }" ] && continue
        ADDEXT_ARGS+=( -addext "$(echo "$line" | tr -d ' ')" )
    done < "$1"
}

# make_root <crt> <key> <CN>
make_root() {
    new_key "$2"
    ext_to_addext openssl/ext_root_ca.cnf
    openssl req -x509 -new -nodes -key "$2" -sha256 -days "$DAYS" -out "$1" \
        -subj "${SUBJ_BASE}/CN=$3" "${ADDEXT_ARGS[@]}"
}

# make_inter <crt> <key> <CN> <ca_crt> <ca_key>
make_inter() {
    new_key "$2"
    openssl req -new -key "$2" -out "${2%.key}.csr" -subj "${SUBJ_BASE}/CN=$3"
    openssl x509 -req -in "${2%.key}.csr" -CA "$4" -CAkey "$5" -CAcreateserial \
        -out "$1" -days "$DAYS" -sha256 \
        -extfile openssl/ext_inter_ca.cnf
    rm -f "${2%.key}.csr"
}

# make_leaf <out_base> <CN> <ca_crt> <ca_key> <ext_cnf> [days]
make_leaf() {
    local out="$1" cn="$2" ca_crt="$3" ca_key="$4" ext="$5" days="${6:-$DAYS}"
    new_key "${out}.key"
    openssl req -new -key "${out}.key" -out "${out}.csr" -subj "${SUBJ_BASE}/CN=${cn}"
    openssl x509 -req -in "${out}.csr" -CA "$ca_crt" -CAkey "$ca_key" -CAcreateserial \
        -out "${out}.crt" -days "$days" -sha256 -extfile "$ext"
    rm -f "${out}.csr"
}

# make_self_signed <out_base> <CN> <ext_cnf>
make_self_signed() {
    local out="$1" cn="$2" ext="$3"
    new_key "${out}.key"
    ext_to_addext "$ext"
    openssl req -x509 -new -nodes -key "${out}.key" -sha256 -days "$DAYS" \
        -out "${out}.crt" -subj "${SUBJ_BASE}/CN=${cn}" "${ADDEXT_ARGS[@]}"
}

# make_expired_leaf <out_base> <CN> <ca_crt> <ca_key> <ext_cnf>
# Uses `openssl ca` because `openssl x509 -req` cannot backdate a cert.
make_expired_leaf() {
    local out="$1" cn="$2" ca_crt="$3" ca_key="$4" ext="$5"
    new_key "${out}.key"
    openssl req -new -key "${out}.key" -out "${out}.csr" -subj "${SUBJ_BASE}/CN=${cn}"
    openssl ca -batch -notext -config openssl/ca.cnf \
        -cert "$ca_crt" -keyfile "$ca_key" \
        -startdate 20200101000000Z -enddate 20210101000000Z \
        -extfile "$ext" -in "${out}.csr" -out "${out}.crt"
    rm -f "${out}.csr"
}

# Minimal `openssl ca` config (only used to backdate the expired certs).
cat > openssl/ca.cnf <<'EOF'
[ca]
default_ca = CA_default
[CA_default]
dir            = ./_cadb
database       = $dir/index.txt
new_certs_dir  = $dir/newcerts
serial         = $dir/serial
default_md     = sha256
policy         = policy_any
email_in_dn    = no
rand_serial    = yes
unique_subject = no
[policy_any]
commonName             = supplied
countryName            = optional
stateOrProvinceName    = optional
organizationName       = optional
organizationalUnitName = optional
EOF

# --- trust anchors ---------------------------------------------------------
echo "  - root + intermediate CAs"
make_root  ca/root_ca.crt ca/root_ca.key "Secure SunSpec Modbus Root CA"
make_inter ca/server_inter_ca.crt ca/server_inter_ca.key \
           "Secure SunSpec Modbus Server Intermediate CA" ca/root_ca.crt ca/root_ca.key
make_inter ca/client_inter_ca.crt ca/client_inter_ca.key \
           "Secure SunSpec Modbus Client Intermediate CA" ca/root_ca.crt ca/root_ca.key
cat ca/server_inter_ca.crt ca/root_ca.crt > ca/server_ca_chain.crt
cat ca/client_inter_ca.crt ca/root_ca.crt > ca/client_ca_chain.crt

# An unrelated PKI - never added to the trust store - for the
# multiple-PKI and reject-unknown-CA tests (PKI-003, PKI-005).
make_root ca/../foreign_pki/foreign_root_ca.crt foreign_pki/foreign_root_ca.key \
          "Untrusted Foreign Root CA"

# --- valid server certificates (per TLS version) ---------------------------
echo "  - valid server certificates"
for v in tls1_2 tls1_3; do
    make_leaf "server/$v/server_valid" "SunSpecModbusSecurityServer" \
        ca/server_inter_ca.crt ca/server_inter_ca.key openssl/ext_server.cnf
done

# --- invalid server certificates -------------------------------------------
echo "  - invalid server certificates"
make_self_signed server/invalid/server_self_signed "SunSpecModbusSecurityServer" \
    openssl/ext_server.cnf
make_leaf server/invalid/server_no_san "SunSpecModbusSecurityServer" \
    ca/server_inter_ca.crt ca/server_inter_ca.key openssl/ext_server_no_san.cnf
make_leaf server/invalid/server_foreign_ca "SunSpecModbusSecurityServer" \
    foreign_pki/foreign_root_ca.crt foreign_pki/foreign_root_ca.key openssl/ext_server.cnf
make_expired_leaf server/invalid/server_expired "SunSpecModbusSecurityServer" \
    ca/server_inter_ca.crt ca/server_inter_ca.key openssl/ext_server.cnf

# --- valid client certificates: one per mandatory SunSpec role -------------
echo "  - valid client certificates (one per SunSpec role)"
for v in tls1_2 tls1_3; do
    for role in "${ROLES[@]}"; do
        # client_readonly, client_gridservice, client_netadmin, client_superadmin
        case "$role" in
            ReadOnlySunSpec)             name=client_readonly ;;
            GridServiceSunSpec)          name=client_gridservice ;;
            NetworkAdministratorSunSpec) name=client_netadmin ;;
            SuperAdministratorSunSpec)   name=client_superadmin ;;
        esac
        write_client_ext "openssl/_ext_${name}.cnf" "$role"
        make_leaf "client/$v/${name}" "SunSpecModbusSecurityClient-${role}" \
            ca/client_inter_ca.crt ca/client_inter_ca.key "openssl/_ext_${name}.cnf"
    done
done

# --- invalid client certificates -------------------------------------------
echo "  - invalid client certificates"
# No role extension at all (SunSpecTCP-32: server must reject with exception 01).
write_client_ext openssl/_ext_no_role.cnf ""
make_leaf client/invalid/client_no_role "SunSpecModbusSecurityClient-NoRole" \
    ca/client_inter_ca.crt ca/client_inter_ca.key openssl/_ext_no_role.cnf
# Role encoded as IA5String instead of UTF8String (violates SunSpecTCP-30).
write_client_ext openssl/_ext_malformed_role.cnf "ReadOnlySunSpec" IA5String
make_leaf client/invalid/client_malformed_role "SunSpecModbusSecurityClient-MalformedRole" \
    ca/client_inter_ca.crt ca/client_inter_ca.key openssl/_ext_malformed_role.cnf
# Self-signed (not chained to a trusted CA).
write_client_ext openssl/_ext_readonly_ss.cnf "ReadOnlySunSpec"
make_self_signed client/invalid/client_self_signed "SunSpecModbusSecurityClient-SelfSigned" \
    openssl/_ext_readonly_ss.cnf
# Signed by the untrusted foreign CA.
make_leaf client/invalid/client_foreign_ca "SunSpecModbusSecurityClient-Foreign" \
    foreign_pki/foreign_root_ca.crt foreign_pki/foreign_root_ca.key openssl/_ext_readonly_ss.cnf
# Expired.
make_expired_leaf client/invalid/client_expired "SunSpecModbusSecurityClient-Expired" \
    ca/client_inter_ca.crt ca/client_inter_ca.key openssl/_ext_readonly_ss.cnf

# --- tidy up ---------------------------------------------------------------
rm -rf _cadb ca/*.srl foreign_pki/*.srl openssl/_ext_*.cnf
find . -name '*.srl' -delete

echo "Done. Secure SunSpec Modbus TLS test PKI written under $(pwd)"

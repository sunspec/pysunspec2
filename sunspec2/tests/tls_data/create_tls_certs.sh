# Generate a Certificate Authority (CA)
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt -config ca.cnf

# Generate Intermediate CA for Server
openssl genrsa -out server_inter_ca.key 2048
openssl req -new -key server_inter_ca.key -out server_inter_ca.csr -subj "/C=US/ST=STATE/L=LOCAL/O=ORG/OU=SUBORG/CN=INTER-CA-SERVER"
openssl x509 -req -in server_inter_ca.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server_inter_ca.crt -days 3650 -sha256 -extfile intermediate_ca.cnf -extensions v3_ca

# Generate Intermediate CA for Client
openssl genrsa -out client_inter_ca.key 2048
openssl req -new -key client_inter_ca.key -out client_inter_ca.csr -subj "/C=US/ST=STATE/L=LOCAL/O=ORG/OU=SUBORG/CN=INTER-CA-CLIENT"
openssl x509 -req -in client_inter_ca.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client_inter_ca.crt -days 3650 -sha256 -extfile intermediate_ca.cnf -extensions v3_ca

# Generate a Server Certificate signed by Server Intermediate CA
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -config server.cnf
openssl x509 -req -in server.csr -CA server_inter_ca.crt -CAkey server_inter_ca.key -CAcreateserial -out server.crt -days 3650 -sha256 -extensions SAN -extfile server.cnf

# Generate a Client Certificate signed by Client Intermediate CA
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj "/C=US/ST=STATE/L=LOCAL/O=ORG/OU=CLIENTORG/CN=SunSpecModbusSecurityClient"
openssl x509 -req -in client.csr -CA client_inter_ca.crt -CAkey client_inter_ca.key -CAcreateserial -out client.crt -days 3650 -sha256 -extfile client.cnf -extensions v3_req

# Create full chain files for client and server
cat server_inter_ca.crt ca.crt > server_ca_chain.crt
cat client_inter_ca.crt ca.crt > client_ca_chain.crt

# Print out the server and client certificate in human readable format
echo "Server Certificate:"
openssl x509 -in server.crt -text -noout
echo "Client Certificate:"
openssl x509 -in client.crt -text -noout

# Test the server with openssl
# openssl s_server -accept 8502 -cert server.crt -key server.key -CAfile server_ca_chain.crt -Verify 1 &
# openssl s_client -connect localhost:8502 -CAfile client_ca_chain.crt -cert client.crt -key client.key
# pkill -f "openssl s_server"
# Generate a Certificate Authority (CA)
openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt -config ca.cnf

# Generate a Server Certificate
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "//CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 3650 -sha256

# Generate a Client Certificate
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -subj "//CN=Test Client"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 3650 -sha256
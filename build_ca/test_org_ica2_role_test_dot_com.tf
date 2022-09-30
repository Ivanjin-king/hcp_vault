resource "vault_pki_secret_backend_role" "role" {
 backend            = vault_mount.test_org_v1_ica2_v1.path
 name               = "test-dot-com-subdomain"
 ttl                = "48h"
 allow_ip_sans      = true
 key_type           = "rsa"
 key_bits           = 2048
 key_usage          = [ "DigitalSignature","KeyEncipherment"]
 allow_any_name     = true
 allow_localhost    = false
 allowed_domains    = ["preprod.local"]
 allow_bare_domains = true
 allow_subdomains   = true
 server_flag        = true
 client_flag        = true
 no_store           = true
 country            = ["NZ"]
 locality           = ["CHC"]
 province           = ["CHC"]
}

#https://www.vaultproject.io/api-docs/secret/pki#create-update-role
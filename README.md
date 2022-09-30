This is a roadmap of a solution I recently work on, you can find why and how Hashicorp Vault, Consul and CTS are involved gradually.

<img src="https://raw.githubusercontent.com/Ivanjin-king/hcp_vault/master/temp/test.png">

The diagram initially target remote hosts/VMs for PKI automation via a CI/CD flavour in order to eliminate the massive pain of service outage in an organisation which lack the visibility of certificate validity.
- The architecture start from following iaC principle, pipelines are triggered daily, weekly or manually to start Cert Mgmt containers via terraform first.  Apps are then loaded into container according to defined operation flows in pipeline. The containers are ephemeral, will go way once job done.
- App of Cert Discovery only need to be performed once against each domain/group, the current state of certificates is sent to DB as source of true to be consumed by apps Cert Validity Check and Cert Deployment later .
- App of Cert Validity Check starts to query DB on a periodic time to to find the certificates on a specific host which don't comply with security policy, eg, some certs will expire in 10 Days.
- App Cert Deployment started to delete, renew, rebind the certificates depending on result of  app Cert Validity Check.

### **The challenge in V1:**
- App Cert Discovery and Cert Deployment need to connect to many hosts maintained by various team to read/write, credentials and variables need to be protected thoroughly.  Although the secrets and variables can be stored in Git Tools and pass into apps as environment variable, a professional secret server is beneficial.
- In a traditional way, in order to get a valid certificate, a private key for host has to be generated first, then a CSR  has to be generated with the private key. The CA returns a valid certificate until receiving a CSR. What a cumbersome process which has been frustrating. What we really want is just a pem coded file containing certificate, key and trusted chain. 
- When transporting a certificate and key from container to windows machine with a PFX file,  we absolutely want the PFX file to be protected by a strong password to avoid private key leakage. Although the lifetime of the password is less than 1 sec, we need a solid password generators, and passwords can be obtained by an API request programmatically.

This is where HCP vault  in version 2(dark grey) comes through , it can resolve the challenges above. In addition, it can be intermediate of Internal CA  signing cert for client as well as proxy of external CA for cert request, renew, etc.  CertBot is added in v2 working together with Vault communicating with external CA like Let's encrypts, RabbitMQ is message broker to handle requests.

### **The challenge in V2:**  
- While version  2 is running well, I wonder if communication between apps in cert mgmt container, Vault, RabbitMQ, CertBot, and DB are secure, the vault could be cloud based, the DB could be in another Datacenter.  the secure communication becomes a new challenge to achieve the Zero trust network.
- How can I track one of service failure.

I soon realized that this is a service mesh in the solution and this is where HCP Consul in version 3(blue) comes through to securing the mesh, facilitating service discovery, health checking, policy enforcement, and other similar operational concerns.

### **The challenge in V3:**
- Apps in Cert mgmt containers need to reach out to an amount of remote hosts in various domain, The ports on the firewall need to be opened to allow  for access. Most company have ticket driven system, say, you create a ticket to operation, then the ticket is assigned to an engineer in security team who then manually configure the firewall as required. The process usually takes long long time,consume valuable resources, and increase human errors.
This is where CTS (Consul-Terraform-Sync) in version 4(red)comes through that can automate firewall change base on info on Consul..

I'm currently working on V4, looking forward to see V5 that bring some new challenge. Although this solution is talking about PKI automation solution, this is a common platform/ framework for other solutions, you just need to replace the apps in the container.

# maestr-image
Maester Image Orchestrator

## Description
This project aims to manage operating system images from different public sources (ex. ubuntu and centos) and keep them up to date. It uses webscraping to get the latest builds of the images and stores them locally or in S3 compatible storage.

Using a customizable schema that defines what image, how many versions and schedule, it will strive to keep that at the destionation location (ex. Glance).


## Q&A
**Question:** Why is this a thing?

Stop updating images manually! Automation is key.


## Tasks
- [ ] Support Ubuntu (https://cloud-images.ubuntu.com/releases/)
- [ ] Support Ubuntu Minimal (https://cloud-images.ubuntu.com/minimal/releases/)
- [ ] Support Centos (https://cloud.centos.org/centos/)
- [ ] Support RedHat
- [ ] Support Fedora
- [ ] Support Debian
- [ ] Support CoreOS
- [ ] Support Cirros
- [ ] Support Windows Server (Manually. Maybe automatically in the future)
- [ ] Download to local filesystem
- [ ] Download to S3 compatible APIs
- [ ] Upload to Openstack Glance
- [ ] Customizable schema for rotating image versions
- [ ] Implement simple web frontend


## Environment variables (development, only postgres running as docker)
    FLASK_APP=api
    FLASK_ENV=development
    
    POSTGRES_URL=localhost
    POSTGRES_USER=postgres
    POSTGRES_PW=postgres
    POSTGRES_DB=tuwio
    
    OS_REGION=GOT
    OS_URL=http://10.222.0.110:5000/v3
    OS_CRED_ID=admin
    OS_CRED_SECRET=PASSWORD
    OS_PROJECT_ID=39a31564c5714a358b5294e2642fb39f
    OS_USER_DOMAIN_ID=22c2c9aa684445c0a7b366e810828ad9


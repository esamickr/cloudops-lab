# CloudOps Lab

CloudOps Lab, Linux, networking, containerization, cloud infrastructure, Infrastructure as Code (IaC), CI/CD, Kubernetes ve monitoring konularını uygulamalı olarak öğrenmek amacıyla geliştirilen bir çalışma projesidir.

Proje boyunca basit bir Python Flask API farklı altyapı ortamlarında çalıştırılarak deployment, networking, containerization ve automation konuları uygulamalı olarak ele alınmaktadır.

---

## Project Architecture

Mevcut AWS deployment mimarisi:

```text
Client
   |
   | HTTP :80
   v
AWS Security Group
   |
   v
EC2 Ubuntu Server
   |
   v
Nginx :80
   |
   | Reverse Proxy
   v
Docker published port :5000
   |
   v
Flask API Container
```

Nginx, EC2 sunucusu üzerinde reverse proxy olarak çalışmaktadır.

Flask uygulaması ise Docker container içerisinde çalışmaktadır.

Bu yapı sayesinde dış istemciler uygulamaya doğrudan `:5000` portundan erişmek yerine HTTP üzerinden `:80` portuna bağlanmaktadır.

---

## Application

Proje içerisinde basit bir Python Flask API bulunmaktadır.

API'nin amacı karmaşık bir backend uygulaması geliştirmek değil, farklı deployment ve altyapı teknolojilerini uygulamalı olarak kullanabilecek bir servis sağlamaktır.

### Endpoints

#### GET /health

Uygulamanın çalışır durumda olup olmadığını kontrol etmek için kullanılır.

Örnek response:

```json
{
  "service": "cloudops-lab",
  "status": "healthy",
  "version": "1.0"
}
```

#### GET /status

Uygulamanın çalışma durumu hakkında temel bilgiler sağlar.

---

# Learning Progress

## Day 1 — Linux, Networking and Reverse Proxy

İlk aşamada Linux sunucu yönetimi, temel networking ve reverse proxy konuları üzerinde çalışılmıştır.

Çalışılan konular:

- Ubuntu Server
- Linux dosya sistemi
- Temel Linux komutları
- Dosya ve dizin yönetimi
- Kullanıcı ve izin kavramları
- IP adresleri
- Network interface'leri
- TCP/IP
- Port kavramı
- SSH
- Servis yönetimi
- systemd
- Nginx
- Reverse proxy
- Git
- GitHub

### Reverse Proxy

Nginx, istemciden gelen HTTP isteklerini Flask uygulamasına yönlendirmek için reverse proxy olarak yapılandırılmıştır.

İstek akışı:

```text
Client
   |
   | HTTP :80
   v
Nginx
   |
   | proxy_pass
   v
Flask :5000
```

---

## Day 2 — Docker and Containerization

İkinci aşamada uygulama Docker kullanılarak container haline getirilmiştir.

Çalışılan konular:

- Docker Engine
- Docker Image
- Docker Container
- Dockerfile
- Container lifecycle
- Port mapping
- Docker network kavramı
- Docker volume kavramı
- Docker Compose
- Container logları
- Container içerisinde komut çalıştırma
- Nginx ve Flask servislerinin birlikte çalıştırılması

Python Flask uygulaması için Docker image oluşturulmuş ve container içerisinde çalıştırılmıştır.

Örnek:

```bash
docker build -t cloudops-api:1.0 .
```

Container çalıştırma:

```bash
docker run -d \
  --name cloudops-api \
  -p 5000:5000 \
  cloudops-api:1.0
```

Uygulama:

```text
Host :5000
    |
    v
Docker Container :5000
    |
    v
Flask Application
```

Docker Compose ile birden fazla servisin birlikte yönetilmesi de çalışılmıştır.

---

## Day 3 — AWS EC2 Deployment

Üçüncü aşamada uygulama AWS üzerinde bulunan bir EC2 Ubuntu Server ortamına deploy edilmiştir.

### AWS Environment

Çalışılan AWS bileşenleri:

- AWS EC2
- Ubuntu Server
- VPC
- Subnet
- Security Group
- Public IP
- Private IP
- SSH
- Docker
- Nginx

### Deployment

Python Flask uygulaması AWS EC2 üzerinde bulunan Ubuntu Server üzerine deploy edilmiştir.

Uygulama Docker container içerisinde çalıştırılmış ve Nginx reverse proxy olarak yapılandırılmıştır.

Deployment akışı:

```text
Windows Client
      |
      | HTTP :80
      v
AWS Security Group
      |
      v
EC2 Ubuntu Server
      |
      v
Nginx :80
      |
      | Reverse Proxy
      v
Docker :5000
      |
      v
Flask Container
```

### Network Configuration

Uygulama başlangıçta TCP/5000 portu üzerinden doğrudan erişilebilir şekilde test edilmiştir.

Daha sonra Nginx reverse proxy yapılandırılarak uygulamaya HTTP üzerinden TCP/80 portu ile erişim sağlanmıştır.

Bu yapı ile uygulamanın `5000` portunun doğrudan internet üzerinden erişilebilir olması gereksiz hale getirilmiştir.

### Verification

Uygulama Windows istemcisinden EC2 public IP adresi üzerinden test edilmiştir:

```bash
curl.exe http://<EC2-PUBLIC-IP>/health
```

Başarılı response:

```json
{
  "service": "cloudops-lab",
  "status": "healthy",
  "version": "1.0"
}
```

Bu test ile aşağıdaki akış doğrulanmıştır:

```text
Client
   |
   v
AWS Security Group
   |
   v
EC2
   |
   v
Nginx
   |
   v
Flask
   |
   v
Docker Container
```

---

# Repository Structure

```text
cloudops-lab/
├── app/
├── linux/
├── project/
│   ├── Dockerfile
│   ├── app.py
│   ├── compose.yaml
│   ├── nginx/
│   └── requirements.txt
└── README.md
```

---

# Technologies

- Linux
- Ubuntu Server
- Python
- Flask
- Docker
- Docker Compose
- Nginx
- Git
- GitHub
- AWS EC2
- TCP/IP

---

# Git Workflow

Projede Git kullanılarak yapılan çalışmalar versiyonlanmaktadır.

Temel workflow:

```bash
git add .
git commit -m "Description of changes"
git push
```

Projenin gelişimi Git commit geçmişi üzerinden takip edilmektedir.

Örnek commitler:

```text
Day 1: Linux networking and reverse proxy setup
Day 2: Docker containerization and Compose setup
```

---

# Future Work

Projenin sonraki aşamalarında aşağıdaki teknolojilerin uygulamalı olarak eklenmesi planlanmaktadır:

- Terraform
- Infrastructure as Code
- AWS infrastructure provisioning
- GitHub Actions
- CI/CD
- Kubernetes
- Kubernetes Deployment
- Kubernetes Service
- Helm
- Prometheus
- Grafana
- Monitoring and observability
- OpenStack temel kavramları

Hedef mimari:

```text
                 GitHub
                    |
                    v
             GitHub Actions
                    |
                    v
              Docker Image
                    |
                    v
              Kubernetes
                    |
          +---------+---------+
          |                   |
          v                   v
       Flask App          Monitoring
                              |
                              v
                       Prometheus
                              |
                              v
                           Grafana
```

---

# Purpose

Bu proje, Cloud Engineer / Platform Engineering alanında kullanılan temel teknolojileri tek bir uygulama üzerinde birleştirerek pratik deneyim kazanmak amacıyla geliştirilmektedir.

Proje sürecinde yalnızca araçların kurulması değil, bu araçların birbirleriyle nasıl çalıştığı, network iletişimi, deployment süreçleri, otomasyon ve sistem yönetimi gibi konuların anlaşılması hedeflenmektedir.

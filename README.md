# CloudOps Lab

CloudOps Lab; Linux, Docker, Docker Compose, AWS, Terraform, GitHub Actions, Kubernetes, Minikube, Helm, Prometheus ve Grafana kullanılarak geliştirilen uçtan uca bir Cloud/DevOps projesidir.

Proje boyunca aynı uygulama farklı çalışma ortamlarına taşınarak; Linux üzerinde çalıştırılmasından container haline getirilmesine, AWS üzerinde deploy edilmesinden Infrastructure as Code yaklaşımına, CI sürecinden Kubernetes orchestration ve monitoring altyapısına kadar ilerleyen bir yapı oluşturulmuştur.

## Genel Mimari

````text
                              GitHub
                                 │
                                 ▼
                         GitHub Actions
                              CI
                                 │
                                 ▼
                         Python Application
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
              Docker / Compose          AWS / Terraform
                    │
                    ▼
                Kubernetes
                 Minikube
                    │
             ┌──────┴──────┐
             │             │
             ▼             ▼
         Deployment      Service
             │
        ┌────┴────┐
        │         │
        ▼         ▼
      Pod 1     Pod 2
        │         │
        └────┬────┘
             │
             ▼
        CloudOps API
             │
       ┌─────┼─────────┐
       │     │         │
       ▼     ▼         ▼
    /health /status  /metrics
                         │
                         ▼
                     Prometheus
                         │
                         ▼
                      Grafana
`````

---

# 1. Gün — Linux, Networking ve Reverse Proxy

Projenin ilk aşamasında uygulamanın çalışacağı Ubuntu Server ortamı hazırlanmış ve uygulamanın işletim sistemi ile ağ katmanındaki çalışma mantığı ele alınmıştır.

Bu aşamada uygulamanın yalnızca çalıştırılması değil; hangi IP adresinde dinlediği, hangi portu kullandığı, başka bir makineden nasıl erişildiği ve HTTP trafiğinin uygulamaya nasıl yönlendirildiği üzerinde çalışılmıştır.

## Linux Ortamı

Çalışma ortamı Ubuntu Server üzerinde hazırlanmıştır.

Linux üzerinde özellikle aşağıdaki konular uygulanmıştır:

* Dosya sistemi ve çalışma dizinleri
* Paket yönetimi
* Network interface'leri
* IP adresleri
* Portlar
* SSH
* Process ve servis mantığı
* Temel ağ kontrolleri

Network interface'lerini incelemek için:

```bash
ip addr
```

komutu kullanılmıştır.

Bu komut ile sistemdeki network interface'leri, IPv4 adresleri ve interface durumları incelenmiştir.

## IP ve Port Yapısı

Uygulama `8000` portunda çalışacak şekilde yapılandırılmıştır.

Bir uygulamanın bir sunucuda çalışıyor olması tek başına dışarıdan erişilebilir olduğu anlamına gelmez. Uygulamanın hangi IP adresinde dinlediği ve hangi portu kullandığı da önemlidir.

Projede bu ilişki:

```text
Client
   │
   │ HTTP
   ▼
Server IP : 8000
   │
   ▼
Python Application
```

şeklinde ele alınmıştır.

## Reverse Proxy

İlk aşamada Nginx reverse proxy olarak kullanılmıştır.

Temel yapı:

```text
Client
   │
   │ HTTP :80
   ▼
 Nginx
   │
   │ Proxy
   ▼
Application :8000
```

Nginx dışarıdan gelen HTTP isteklerini uygulamanın çalıştığı `8000` portuna yönlendirmiştir.

Reverse proxy kullanımı sayesinde istemci ile uygulama arasında ayrı bir web sunucusu katmanı oluşturulmuştur.

Bu yapı daha sonraki Docker ve Kubernetes aşamalarında kullanılacak olan servis yönlendirme ve trafik yönetimi mantığının temelini oluşturmuştur.

---

# 2. Gün — Docker ve Docker Compose

İkinci aşamada Linux üzerinde çalışan uygulama Docker container haline getirilmiştir.

Buradaki temel amaç, uygulamanın yalnızca kaynak kodunun değil, çalışması için ihtiyaç duyduğu ortamın da taşınabilir hale getirilmesidir.

Python sürümü, bağımlılıklar ve uygulamanın çalışma biçimi Docker image içerisinde tanımlanmıştır.

## Docker Image

Uygulamanın container haline getirilmesi için Dockerfile kullanılmıştır.

Temel akış:

```text
Python Application
       │
       ▼
   Dockerfile
       │
       ▼
 Docker Image
       │
       ▼
  Container
```

Dockerfile içerisinde uygulamanın çalışma ortamı, çalışma dizini, gerekli dosyaları ve uygulamanın çalıştırılma komutu tanımlanmıştır.

Docker image oluşturulduktan sonra bu image üzerinden container çalıştırılmıştır.

## Container ve Port Mapping

Uygulama container içerisinde `8000` portunda çalışmaktadır.

Host ile container arasında port eşlemesi yapılarak uygulamanın dışarıdan erişilebilir olması sağlanmıştır.

```text
Host :8000
    │
    ▼
Container :8000
    │
    ▼
Python Application
```

Bu yapı sayesinde uygulamanın container içerisinde çalışması ile host üzerinden erişilmesi arasındaki ilişki uygulanmıştır.

## Docker Compose

Birden fazla servisin birlikte yönetilmesi için Docker Compose kullanılmıştır.

Projede uygulama ve Nginx servislerinin aynı Docker ortamında çalışması ve birbirleriyle Docker network üzerinden iletişim kurması uygulanmıştır.

```text
Client
   │
   ▼
Nginx Container
   │
   │ Docker Network
   ▼
Application Container
   │
   ▼
Python API
```

Buradaki önemli nokta, container'ların birbirleriyle doğrudan host makinenin IP adresi üzerinden değil Docker tarafından oluşturulan network üzerinden haberleşebilmesidir.

Bu aşamada ayrıca container, image, port mapping ve Docker network kavramları birlikte uygulanmıştır.

---

# 3. Gün — AWS EC2 Üzerinde Deployment

Üçüncü aşamada uygulama lokal Linux ortamından çıkarılarak AWS üzerinde çalışan bir EC2 instance'a taşınmıştır.

Böylece daha önce lokal ortamda oluşturulan Linux ve Docker yapısı gerçek bir cloud sunucu üzerinde uygulanmıştır.

Genel deployment akışı:

```text
Local Environment
       │
       ▼
 Docker Image
       │
       ▼
 AWS EC2
       │
       ▼
 Linux Server
       │
       ▼
 Docker Container
       │
       ▼
 Application
```

## EC2

AWS EC2 üzerinde Linux tabanlı bir sunucu ortamı hazırlanmıştır.

EC2 üzerinde Docker kurulumu gerçekleştirilmiş ve uygulama container olarak çalıştırılmıştır.

Bu aşamada önceki günlerde öğrenilen:

* Linux
* SSH
* IP adresleri
* Portlar
* Docker
* Container

kavramları gerçek bir cloud ortamında birlikte kullanılmıştır.

## SSH

EC2 instance'a uzaktan erişim SSH üzerinden gerçekleştirilmiştir.

```text
Developer
    │
    │ SSH
    ▼
AWS EC2
    │
    ▼
Linux Server
```

Bu sayede uzak sunucuya bağlanılarak Docker ve uygulama yönetimi yapılmıştır.

## Network ve Erişim

EC2 üzerinde çalışan uygulamaya erişebilmek için yalnızca container'ın çalışması yeterli değildir.

Cloud ortamındaki network yapılandırmasının ve gerekli port erişimlerinin de doğru olması gerekir.

Bu aşamada uygulamanın:

```text
Internet
    │
    ▼
AWS Network
    │
    ▼
EC2
    │
    ▼
Docker Container
    │
    ▼
Application
```

şeklindeki erişim zinciri uygulanmıştır.

---

# 4. Gün — Terraform ve Infrastructure as Code

Dördüncü aşamada AWS altyapısının manuel olarak yönetilmesi yerine Terraform ile kod olarak tanımlanması uygulanmıştır.

Bu yaklaşım Infrastructure as Code (IaC) olarak adlandırılır.

Temel yaklaşım:

```text
Terraform Configuration
          │
          ▼
   terraform init
          │
          ▼
    terraform plan
          │
          ▼
   terraform apply
          │
          ▼
      AWS Resources
```

Terraform sayesinde altyapı kaynaklarının hangi özelliklerle oluşturulacağı kod içerisinde tanımlanabilir.

Bu yaklaşım altyapının tekrar oluşturulmasını, değişikliklerin takip edilmesini ve yapılandırmanın versiyon kontrolünde tutulmasını kolaylaştırır.

## Terraform Dosya Yapısı

Projede Terraform yapılandırması:

```text
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
└── .terraform.lock.hcl
```

şeklindedir.

### main.tf

Terraform provider ve AWS kaynaklarının temel yapılandırmasının bulunduğu dosyadır.

### variables.tf

Altyapıda kullanılacak değişkenlerin tanımlandığı dosyadır.

### outputs.tf

Terraform tarafından oluşturulan kaynaklarla ilgili çıktıların tanımlandığı dosyadır.

### .terraform.lock.hcl

Terraform provider bağımlılıklarının kullanılan sürümlerinin sabitlenmesini sağlar.

## Terraform Workflow

Terraform ile temel çalışma akışı:

```bash
terraform init
terraform plan
terraform apply
```

`terraform init`, Terraform çalışma ortamını ve provider bağımlılıklarını hazırlar.

`terraform plan`, uygulanacak değişiklikleri gerçekleştirmeden önce gösterir.

`terraform apply`, planlanan değişiklikleri AWS ortamına uygular.

Terraform state ve değişken dosyaları repository'ye gönderilmemektedir.

---

# 5. Gün — GitHub Actions ile CI

Beşinci aşamada projenin GitHub repository'sine gönderilen değişikliklerinin otomatik olarak kontrol edilmesi için GitHub Actions kullanılmıştır.

Amaç, kodun repository'ye gönderilmesinden sonra temel kontrollerin manuel olarak çalıştırılmasına gerek kalmadan CI ortamında gerçekleştirilmesidir.

Temel akış:

```text
Developer
    │
    ▼
git push
    │
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Environment
    ├── Dependencies
    └── Tests
```

Projede workflow:

```text
.github/
└── workflows/
    └── ci.yml
```

dosyası üzerinden yönetilmektedir.

Bu yapı ile Git repository'sine yapılan değişikliklerin otomatik bir kontrol sürecinden geçirilmesi sağlanmıştır.

CI yaklaşımı özellikle ilerleyen aşamalarda Docker ve Kubernetes gibi deployment süreçleriyle birleştirilebilecek bir temel oluşturmuştur.

---

# 6. Gün — Kubernetes, Minikube ve Helm

Altıncı aşamada uygulama Docker container seviyesinden Kubernetes orchestration ortamına taşınmıştır.

Lokal Kubernetes ortamı olarak Minikube kullanılmıştır.

Genel yapı:

```text
Docker Image
     │
     ▼
   Minikube
     │
     ▼
 Kubernetes
     │
     ├── Namespace
     ├── Deployment
     ├── Pods
     └── Service
```

## Kubernetes Namespace

Uygulama kaynakları:

```text
cloudops
```

namespace'i içerisinde çalıştırılmıştır.

Namespace kullanılması, uygulamaya ait Kubernetes kaynaklarının ayrı bir mantıksal alan içerisinde yönetilmesini sağlar.

## Deployment

Uygulamanın Pod'larının yönetilmesi için Kubernetes Deployment kullanılmıştır.

Deployment iki replica ile çalışmaktadır:

```text
Deployment
    │
    ├── cloudops-api Pod
    │
    └── cloudops-api Pod
```

Mevcut yapı:

```yaml
replicas: 2
```

şeklindedir.

Deployment'ın görevi yalnızca Pod oluşturmak değildir. Tanımlanan replica sayısının korunması ve Pod'ların istenen duruma getirilmesi de Deployment tarafından yönetilir.

## Kubernetes Service

Pod IP adresleri değişebileceği için uygulamaya doğrudan Pod IP'si üzerinden erişmek yerine Kubernetes Service kullanılmıştır.

Service:

```text
Type: ClusterIP
Port: 8000
TargetPort: 8000
```

şeklinde yapılandırılmıştır.

İletişim:

```text
Client
   │
   ▼
cloudops-api Service
   │
   ├── Pod 1
   │
   └── Pod 2
```

şeklinde gerçekleşmektedir.

Service, uygulamanın arkasındaki Pod'ların IP adresleri değişse bile sabit bir erişim noktası sağlar.

## Liveness ve Readiness Probes

Uygulamanın Kubernetes tarafından kontrol edilmesi için `/health` endpoint'i kullanılmıştır.

Liveness probe:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: http
```

Readiness probe:

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: http
```

### Liveness

Container'ın çalışmaya devam edip etmediğinin kontrol edilmesini sağlar.

### Readiness

Pod'un trafik almaya hazır olup olmadığının kontrol edilmesini sağlar.

Bu iki kontrol farklı amaçlara hizmet eder:

```text
Process çalışıyor
       ≠
Uygulama trafik almaya hazır
```

Bu nedenle uygulamanın health endpoint'i Kubernetes'in çalışma durumunu değerlendirmesinde kullanılmıştır.

## Minikube Image Yönetimi

Lokal Minikube ortamında kullanılan image:

```text
cloudops-lab:1.2
```

olarak oluşturulmuştur.

Image Minikube ortamına yüklenerek Kubernetes Deployment içerisinde kullanılmıştır.

Deployment tarafında:

```yaml
imagePullPolicy: Never
```

kullanılmasıyla image'ın uzak bir registry'den çekilmesi yerine Minikube ortamında bulunan image'ın kullanılması sağlanmıştır.

---

# 7. Gün — Monitoring, Prometheus, Grafana ve Helm

Yedinci aşamada Kubernetes üzerinde çalışan uygulamanın yalnızca "çalışıyor" durumda olması yerine uygulama hakkında ölçülebilir verilerin toplanması ve görüntülenmesi sağlanmıştır.

Bu aşamada:

* Prometheus
* Grafana
* kube-state-metrics
* node-exporter
* Prometheus Python client
* ServiceMonitor
* Helm

birlikte kullanılmıştır.

---

## Application Metrics

Uygulamaya Prometheus uyumlu metrics endpoint'i eklenmiştir.

Uygulama:

```text
/metrics
```

endpoint'i üzerinden Prometheus formatında metrik üretmektedir.

Uygulamada HTTP isteklerini takip etmek için Counter ve Histogram kullanılmıştır.

### HTTP Request Counter

```text
cloudops_http_requests_total
```

metriği HTTP isteklerinin sayısını takip eder.

Metrik aşağıdaki bilgilerle ayrıştırılır:

```text
method
endpoint
status
```

Bu sayede örneğin farklı endpoint'lere gelen istekler veya HTTP status kodlarına göre request sayıları ayrı ayrı incelenebilir.

### HTTP Request Duration

```text
cloudops_http_request_duration_seconds
```

metriği HTTP request sürelerini ölçmek için Histogram olarak oluşturulmuştur.

Histogram sonucunda Prometheus tarafında:

```text
_bucket
_sum
_count
```

serileri oluşur.

Bu değerler kullanılarak request latency'si hakkında zaman içerisindeki değişimler incelenebilir.

---

# Prometheus

Prometheus, uygulamanın ve Kubernetes ortamının metriklerini toplamak için kullanılmıştır.

Uygulama metrikleri:

```text
CloudOps API
     │
     │ GET /metrics
     ▼
 Prometheus
     │
     ▼
 Time Series Data
```

akışıyla toplanmaktadır.

Prometheus belirli aralıklarla uygulamanın `/metrics` endpoint'ini scrape ederek metrikleri kendi veri yapısında saklar.

---

# ServiceMonitor

Kubernetes üzerinde Prometheus'un uygulamayı otomatik olarak keşfedebilmesi için ServiceMonitor kullanılmıştır.

```text
CloudOps API
     │
     ▼
Kubernetes Service
     │
     ▼
ServiceMonitor
     │
     ▼
Prometheus
```

ServiceMonitor:

```text
k8s/servicemonitor.yaml
```

dosyasında tanımlanmıştır.

Uygulamanın bulunduğu namespace:

```yaml
namespaceSelector:
  matchNames:
    - cloudops
```

olarak belirtilmiştir.

Prometheus'un izleyeceği Service ise:

```yaml
selector:
  matchLabels:
    app: cloudops-api
```

ile seçilmektedir.

Metrics endpoint'i:

```yaml
endpoints:
  - port: http
    path: /metrics
    interval: 15s
```

şeklinde tanımlanmıştır.

Buradaki `http` değeri Kubernetes Service içerisindeki named port ile eşleşmektedir.

---

# Grafana

Grafana, Prometheus tarafından toplanan metriklerin görselleştirilmesi için kullanılmıştır.

Temel monitoring akışı:

```text
Application
     │
     │ Metrics
     ▼
Prometheus
     │
     │ PromQL
     ▼
Grafana
```

Örneğin toplam request sayısını görmek için:

```promql
sum(cloudops_http_requests_total)
```

Request rate:

```promql
rate(cloudops_http_requests_total[5m])
```

Endpoint bazında request rate:

```promql
sum by (endpoint) (
  rate(cloudops_http_requests_total[5m])
)
```

Request'lerin ortalama işlem süresini yaklaşık olarak incelemek için:

```promql
rate(cloudops_http_request_duration_seconds_sum[5m])
/
rate(cloudops_http_request_duration_seconds_count[5m])
```

kullanılabilir.

---

# Helm

Yedinci günün bir diğer önemli kısmında Kubernetes kaynaklarının Helm ile template tabanlı olarak yönetilmesi sağlanmıştır.

Projeye başlangıçta örnek bir Helm chartı eklenmiş ve bu chart Nginx image'ı kullanan standart bir chart yapısına sahipti.

Chart incelendikten sonra mevcut uygulamaya uyarlanmıştır.

Son yapı:

```text
helm/
└── cloudops-lab/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── _helpers.tpl
        ├── deployment.yaml
        └── service.yaml
```

şeklindedir.

Nginx'e ait kullanılmayan:

```text
hpa.yaml
httproute.yaml
ingress.yaml
serviceaccount.yaml
tests/test-connection.yaml
```

gibi örnek template'ler kaldırılmıştır.

Chart artık gerçek CloudOps API uygulamasını hedeflemektedir.

## Helm Values

Uygulamanın replica sayısı ve image bilgisi `values.yaml` üzerinden yönetilmektedir.

Örneğin:

```yaml
replicaCount: 2

image:
  repository: cloudops-lab
  pullPolicy: Never
  tag: "1.2"
```

Service:

```yaml
service:
  type: ClusterIP
  port: 8000
  targetPort: 8000
```

olarak tanımlanmıştır.

Health check'ler de Helm values üzerinden tanımlanmıştır:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: http

readinessProbe:
  httpGet:
    path: /health
    port: http
```

Böylece Kubernetes manifestlerinin önemli parametreleri template içerisine sabit değerler olarak yazılmak yerine Helm üzerinden yönetilebilir hale getirilmiştir.

## Helm Template

Chart'ın oluşturacağı Kubernetes manifestlerini cluster'a uygulamadan görmek için:

```bash
helm template cloudops-api ./helm/cloudops-lab
```

komutu kullanılmıştır.

Bu komut sonucunda Helm'in `values.yaml` ve template'leri kullanarak oluşturacağı Deployment ve Service manifestleri görülebilir.

## Helm Lint

Chart'ın yapısal olarak kontrol edilmesi için:

```bash
helm lint ./helm/cloudops-lab
```

komutu kullanılmıştır.

Son durumda chart:

```text
1 chart(s) linted, 0 chart(s) failed
```

sonucuyla doğrulanmıştır.

---

# Monitoring Namespace

Monitoring bileşenleri uygulamadan ayrı bir Kubernetes namespace içerisinde çalıştırılmıştır.

```text
monitoring
├── Prometheus
├── Grafana
├── Alertmanager
├── kube-state-metrics
└── node-exporter
```

Uygulama ise:

```text
cloudops
├── Deployment
├── Pods
└── Service
```

yapısındadır.

Bu ayrım uygulama workload'ları ile monitoring altyapısının birbirinden ayrılmasını sağlar.

---

# Proje Yapısı

```text
cloudops-lab/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── __init__.py
│   ├── app.py
│   └── requirements.txt
│
├── helm/
│   └── cloudops-lab/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── _helpers.tpl
│           ├── deployment.yaml
│           └── service.yaml
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── servicemonitor.yaml
│
├── linux/
│
├── networking/
│
├── project/
│   ├── Dockerfile
│   ├── app.py
│   ├── compose.yaml
│   ├── requirements.txt
│   └── nginx/
│       └── nginx.conf
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── .terraform.lock.hcl
│
├── tests/
│   └── test_app.py
│
├── Dockerfile.k8s
├── get_helm.sh
├── README.md
└── .gitignore
```

---

# Uygulamayı Çalıştırma

## Python Testleri

Testleri çalıştırmak için:

```bash
python3 -m pytest
```

## Docker Image Oluşturma

Kubernetes için image oluşturmak:

```bash
docker build -t cloudops-lab:1.2 -f Dockerfile.k8s .
```

## Image'ı Minikube'a Yükleme

```bash
minikube image load cloudops-lab:1.2
```

## Kubernetes Kaynaklarını Kontrol Etme

```bash
kubectl get pods -n cloudops
kubectl get deployment -n cloudops
kubectl get svc -n cloudops
```

## Helm Kontrolü

```bash
helm lint ./helm/cloudops-lab
```

```bash
helm template cloudops-api ./helm/cloudops-lab
```

## Uygulamaya Lokal Erişim

Service `ClusterIP` olduğu için lokal erişim amacıyla port-forward kullanılabilir:

```bash
kubectl port-forward -n cloudops svc/cloudops-api 8000:8000
```

Health endpoint:

```bash
curl http://localhost:8000/health
```

Status endpoint:

```bash
curl http://localhost:8000/status
```

Metrics endpoint:

```bash
curl http://localhost:8000/metrics
```

---

# Kullanılan Teknolojiler

| Teknoloji          | Kullanım Alanı                         |
| ------------------ | -------------------------------------- |
| Ubuntu Server      | Linux çalışma ortamı                   |
| Python             | HTTP API                               |
| Nginx              | Reverse proxy                          |
| Docker             | Containerization                       |
| Docker Compose     | Çoklu container yönetimi               |
| AWS EC2            | Cloud compute ortamı                   |
| Terraform          | Infrastructure as Code                 |
| Git                | Versiyon kontrolü                      |
| GitHub             | Source code repository                 |
| GitHub Actions     | CI                                     |
| Kubernetes         | Container orchestration                |
| Minikube           | Lokal Kubernetes ortamı                |
| Helm               | Kubernetes package/template management |
| Prometheus         | Metrics collection                     |
| Grafana            | Metrics visualization                  |
| kube-state-metrics | Kubernetes resource metrics            |
| node-exporter      | Node/system metrics                    |

---

# Sonuç

Proje boyunca aynı uygulama farklı altyapı katmanları üzerinde ilerletilmiştir:

```text
Python Application
       │
       ▼
Linux
       │
       ▼
Nginx Reverse Proxy
       │
       ▼
Docker
       │
       ▼
Docker Compose
       │
       ▼
AWS EC2
       │
       ▼
Terraform
       │
       ▼
GitHub Actions
       │
       ▼
Kubernetes / Minikube
       │
       ├── Deployment
       ├── Pods
       └── Service
              │
              ▼
         Prometheus
              │
              ▼
           Grafana
```

Bu yapı içerisinde uygulamanın çalıştırılması, containerization, cloud deployment, Infrastructure as Code, CI, container orchestration, Kubernetes networking, health checks, Helm templating ve application monitoring süreçleri aynı proje üzerinde uygulanmıştır.

```

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,100:1f6feb&height=170&section=header&text=joejaeyoung&fontSize=44&fontColor=e6edf3&desc=Backend%20%C2%B7%20Infra&descSize=17&descAlignY=64&animation=fadeIn" alt="header" />
</div>

### 고치기 전에 지금 동작부터 못 박아 두는 개발자입니다

SW마에스트로 17기에서 3인 팀의 서버 · 인프라 · 앱 네이티브를 맡아 App Store 출시까지 운영하고 있습니다.
바꾸기 전에 현재 동작을 먼저 증명해 두는 방법에 관심이 많습니다. 특성화 테스트, 계약 테스트, 부하 합격선의 코드화 같은 것들입니다.

<div align="center">
  <a href="mailto:whwodud0303@naver.com"><img src="https://img.shields.io/badge/whwodud0303@naver.com-03C75A?style=flat-square&logo=naver&logoColor=white" alt="email" /></a>
  <img src="https://img.shields.io/badge/숭실대학교_컴퓨터학부-0B4DA2?style=flat-square" alt="school" />
  <img src="https://img.shields.io/badge/42Gyeongsan_Lv_11.24-000000?style=flat-square&logo=42&logoColor=white" alt="42" />
  <img src="https://img.shields.io/badge/SW마에스트로_17기-1f6feb?style=flat-square" alt="swm" />
</div>

<br />

## 무엇을 만들었나

| 프로젝트 | 한 일 | 코드 |
| --- | --- | :--: |
| **gromo** <br/> 집중시간 · 스크린타임 소셜 학습 앱 | 3인 팀 팀장. App Store 출시 후 운영 중. 서버 구조를 재편해 **순환 의존 238 → 0**, 흩어진 **user 조회 57건 → 0**으로 정리하고 ArchUnit으로 빌드에서 강제했습니다. GCP 위에 부하테스트 하네스를 만들어 합격선을 verdict 코드로 고정했습니다 | [org](https://github.com/OneOrThree) <br/> `private` |
| **선착순 쿠폰 발급** <br/> 동시성 제어 3단계 비교 | 100개 쿠폰에 1,000명이 동시에 몰릴 때 정확히 100개만 발급하는 API를 **DB 비관적 락 → Redis 원자적 연산 → Redis + Kafka 비동기**로 세 번 구현하고 같은 부하로 비교했습니다. 정확성은 셋 다 같고 **p95가 967ms → 158ms**로 줄었습니다 | [repo](https://github.com/joejaeyoung/Project-coupon_rush) |
| **XV6 커널 확장 5건** <br/> 파일시스템 · 메모리 · 스케줄러 | inode 크기를 그대로 둔 채 슬롯만 재배분해 **최대 파일 70KB → 약 1GB**. COW 스냅샷은 WAL 트랜잭션 한계를 기능 단위로 쪼개 넘겼고, 역페이지 테이블과 소프트웨어 TLB로 프레임 소유자를 추적했습니다 | [인덱싱](https://github.com/joejaeyoung/OS_Project-MultiLevelFileSystem) · [스냅샷](https://github.com/joejaeyoung/OS_Project-SnapshotCheckpointing) · [IPT](https://github.com/joejaeyoung/OS_Project-PhysicalPageFrameTracking) · [MLFQ](https://github.com/joejaeyoung/OS_Project-MLFQScheduling) · [Stride](https://github.com/joejaeyoung/OS_Project-StrideScheduling) |
| **아이 발자국** <br/> 통학차량 승하차 알림 (K-PaaS) | 팀장. 인증 · 유저 도메인 · 웹소켓과 CI/CD를 맡고 기관 웹을 전담했습니다. 로컬에서만 뜨던 원인이 `.env` 의존이라 환경변수 우선으로 바꾸고 CI 조건을 고정했습니다 | [org](https://github.com/rabbit-snake) |
| **SAP MM CBO** <br/> Procure-to-Pay | 공급업체 마스터 → 구매오더 → 입고 → 송장검증을 ABAP으로 구현했습니다. 취소를 삭제가 아니라 역분개 문서로 남기고 이중 취소를 잔여 수량 합산으로 막았습니다 | [repo](https://github.com/joejaeyoung/SAP-MaterialManagement) |
| **CompatPC** <br/> PC 부품 호환성 전문가 시스템 | 소켓 · 폼팩터를 비트마스크로 인코딩해 AND 한 번으로 호환을 판정하고, 검사마다 번호를 붙여 걸린 이유와 권장 조치를 돌려줍니다 | [repo](https://github.com/joejaeyoung/CompatPC) |
| **42stat** <br/> 42 API 수집 · 통계 | 수집 서비스 2개의 골격과 OAuth 토큰 · 페이지네이션 · 401 리프레시를 맡았습니다. 운영 중입니다 | [repo](https://github.com/42srr/STAT_Server) |

<br />

## 쓰는 것

**Backend**

<img src="https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white" /> <img src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white" /> <img src="https://img.shields.io/badge/JPA-59666C?style=flat-square&logo=hibernate&logoColor=white" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" /> <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white" /> <img src="https://img.shields.io/badge/Redis-FF4438?style=flat-square&logo=redis&logoColor=white" /> <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white" />

**Infra · DevOps**

<img src="https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white" /> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" /> <img src="https://img.shields.io/badge/AWS-FF9900?style=flat-square&logo=amazonwebservices&logoColor=white" /> <img src="https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white" /> <img src="https://img.shields.io/badge/k6-7D64FF?style=flat-square&logo=k6&logoColor=white" /> <img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" /> <img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" />

**System · Mobile**

<img src="https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black" /> <img src="https://img.shields.io/badge/React_Native-61DAFB?style=flat-square&logo=react&logoColor=black" /> <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" /> <img src="https://img.shields.io/badge/Swift-F05138?style=flat-square&logo=swift&logoColor=white" /> <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=flat-square&logo=kotlin&logoColor=white" />

<br />

## AI를 어떻게 쓰나

코드 초안과 리뷰는 맡기고, 보존 항목 · 락 등급 · 배포 순서 같은 판단은 직접 내려 PR 본문에 씁니다.
출력은 뮤테이션 테스트, 3회 재현, 특성화 테스트로 확인합니다.

아래는 실제 세션 전사를 집계한 것입니다. 읽어 들인 토큰의 96%가 캐시 재사용인데, 맥락을 매번 새로 올리지 않도록 작업 단위를 잘라 둔 결과입니다.

<div align="center">
  <img src="https://raw.githubusercontent.com/joejaeyoung/joejaeyoung/main/ai-usage.svg" alt="AI coding usage" width="820" />
</div>

<sub>집계 스크립트는 [`gen_ai_usage.py`](gen_ai_usage.py)에 있습니다. 비용은 공개 API 단가로 환산한 추정치입니다.</sub>

<br />

## 활동

<div align="center">
  <img src="https://ghchart.rshah.org/1f6feb/joejaeyoung" alt="contributions" width="780" />
</div>

<div align="center">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=joejaeyoung&theme=github_dark" height="180" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=joejaeyoung&theme=github_dark" height="180" />
</div>

<div align="center">
  <a href="https://solved.ac/gguldanji_pooh"><img src="http://mazassumnida.wtf/api/v2/generate_badge?boj=gguldanji_pooh" alt="solved.ac" height="150" /></a>
</div>

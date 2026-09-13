<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,100:1f6feb&height=170&section=header&text=joejaeyoung&fontSize=44&fontColor=e6edf3&desc=Backend%20%C2%B7%20Infra&descSize=17&descAlignY=64&animation=fadeIn" alt="header" />
</div>

### 고치기 전에 지금 동작부터 못 박아 두는 개발자입니다

SW마에스트로 17기에서 3인 팀의 서버 · 인프라 · 앱 네이티브를 맡아 App Store 출시까지 운영하고 있습니다.
바꾸기 전에 현재 동작을 먼저 증명해 두는 방법에 관심이 많습니다. 특성화 테스트, 계약 테스트, 부하 합격선의 코드화 같은 것들입니다.

<div align="center">
  <a href="mailto:whwodud0303@naver.com"><img src="https://img.shields.io/badge/whwodud0303@naver.com-03C75A?style=flat-square&logo=naver&logoColor=white" alt="email" /></a>
  <a href="https://www.linkedin.com/in/jaeyoung-jo-a18447306/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="linkedin" /></a>
  <img src="https://img.shields.io/badge/숭실대학교_컴퓨터학부-0B4DA2?style=flat-square" alt="school" />
  <img src="https://img.shields.io/badge/42Gyeongsan_Lv_11.24-000000?style=flat-square&logo=42&logoColor=white" alt="42" />
  <img src="https://img.shields.io/badge/SW마에스트로_17기-1f6feb?style=flat-square" alt="swm" />
</div>

<br />

## 📦 무엇을 만들었나

| | 프로젝트 | 남긴 것 | 코드 |
| :--: | --- | --- | :--: |
| 📱 | **gromo** <br/> <sub>집중시간 · 스크린타임 소셜 학습 앱</sub> | 3인 팀 팀장, App Store 운영 중 <br/> 순환 의존 **238 → 0** · user 조회 **57건 → 0** <br/> <sub>ArchUnit으로 빌드에서 강제, GCP 부하 하네스로 합격선을 코드화</sub> | <a href="https://docs.oneorthree.world">팀 문서</a> <br/> <a href="https://github.com/OneOrThree">org</a> <sub>private</sub> |
| 🎟️ | **선착순 쿠폰 발급** <br/> <sub>동시성 제어 3단계 비교</sub> | p95 **967ms → 158ms** (처리량 4.2배) <br/> <sub>DB 비관적 락 → Redis 원자적 연산 → Redis + Kafka. 세 번 구현해 같은 부하로 비교, 정확성은 셋 다 동일</sub> | <a href="https://github.com/joejaeyoung/Project-coupon_rush">repo</a> |
| 🧬 | **XV6 커널 확장 5건** <br/> <sub>파일시스템 · 메모리 · 스케줄러</sub> | 최대 파일 **70KB → 약 1GB** <br/> <sub>inode 크기는 두고 슬롯만 재배분. COW 스냅샷, 역페이지 테이블 + SW TLB, 스케줄러 2종</sub> | <a href="https://github.com/joejaeyoung/OS_Project-MultiLevelFileSystem">인덱싱</a> · <a href="https://github.com/joejaeyoung/OS_Project-SnapshotCheckpointing">스냅샷</a> <br/> <a href="https://github.com/joejaeyoung/OS_Project-PhysicalPageFrameTracking">IPT</a> · <a href="https://github.com/joejaeyoung/OS_Project-MLFQScheduling">MLFQ</a> · <a href="https://github.com/joejaeyoung/OS_Project-StrideScheduling">Stride</a> |
| 🚌 | **아이 발자국** <br/> <sub>통학차량 승하차 알림 (K-PaaS)</sub> | 팀장, 인증 · 웹소켓 · CI/CD · 기관 웹 전담 <br/> <sub>로컬에서만 뜨던 원인이 `.env` 의존이라 환경변수 우선으로 바꾸고 CI 조건을 고정</sub> | <a href="https://github.com/rabbit-snake">org</a> |
| 🧾 | **SAP MM CBO** <br/> <sub>Procure-to-Pay</sub> | 취소를 삭제가 아니라 **역분개 문서**로 <br/> <sub>공급업체 → 구매오더 → 입고 → 송장검증을 ABAP으로. 이중 취소는 잔여 수량 합산으로 차단</sub> | <a href="https://github.com/joejaeyoung/SAP-MaterialManagement">repo</a> |
| 🖥️ | **CompatPC** <br/> <sub>PC 부품 호환성 전문가 시스템</sub> | 소켓 · 폼팩터를 **비트마스크 AND 한 번**으로 판정 <br/> <sub>검사마다 번호를 붙여 걸린 이유와 권장 조치를 돌려줌</sub> | <a href="https://github.com/joejaeyoung/CompatPC">repo</a> |
| 📊 | **42stat** <br/> <sub>42 API 수집 · 통계</sub> | 수집 서비스 2개 골격 · OAuth · 페이지네이션 <br/> <sub>401 리프레시 루프까지. 운영 중</sub> | <a href="https://github.com/42srr/STAT_Server">repo</a> |

<br />

## 🛠 쓰는 것

**Backend**

<img src="https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white" /> <img src="https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white" /> <img src="https://img.shields.io/badge/JPA-59666C?style=flat-square&logo=hibernate&logoColor=white" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" /> <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white" /> <img src="https://img.shields.io/badge/Redis-FF4438?style=flat-square&logo=redis&logoColor=white" /> <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white" />

**Infra · DevOps**

<img src="https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white" /> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" /> <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" /> <img src="https://img.shields.io/badge/AWS-FF9900?style=flat-square" /> <img src="https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white" /> <img src="https://img.shields.io/badge/k6-7D64FF?style=flat-square&logo=k6&logoColor=white" /> <img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" /> <img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" />

**System · Mobile**

<img src="https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black" /> <img src="https://img.shields.io/badge/React_Native-61DAFB?style=flat-square&logo=react&logoColor=black" /> <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" /> <img src="https://img.shields.io/badge/Swift-F05138?style=flat-square&logo=swift&logoColor=white" /> <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=flat-square&logo=kotlin&logoColor=white" />

<br />

## 🤖 AI를 어떻게 쓰나

도구를 쓴다는 말은 이제 정보가 아니라고 생각합니다. 어디까지 맡기고 어디부터 직접 판단했는지, 그리고 그 출력을 무엇으로 검증했는지가 남는 부분이라고 봅니다.

**맡기는 것 / 직접 하는 것**

| | |
| --- | --- |
| 맡김 | 코드 초안, 리팩터링 후보 찾기, 반복 수정, 1차 리뷰 |
| 직접 | 보존해야 할 항목이 무엇인지, 락 등급, 배포 순서, 롤백 경로, 무엇을 안 할지 |

판단은 PR 본문에 제가 씁니다. 남는 건 도구 이름이 아니라 그 문장입니다.

**검증 방법**

- **뮤테이션** — 조회 계층을 옮긴 뒤 예외 코드를 일부러 바꾸고 배타 락을 내려봤는데 테스트 1,895건이 전부 초록이었습니다. 통과가 보존을 뜻하지 않는다는 뜻이라, 전용 테스트 9건을 추가해 락 소실 2건과 예외 변조 1건이 잡히는 것까지 확인했습니다.
- **3회 재현** — 돈 경로 결함 3건은 옛 동작을 임시로 되살려 3회 모두 실패하는 것을 본 뒤에 고쳤습니다.
- **특성화 테스트** — 1,792줄 화면에서 세션 엔진을 떼어낼 때, 손대기 전에 현재 동작을 9테스트 · 8계약으로 먼저 고정하고 이식 후 diff 0을 확인했습니다.

**AI가 틀렸고 제가 잡은 것**

> 기관 웹 화면은 생성 코드로 시작했는데, API 주소를 빌드 시점에 박아 넣는 구조였습니다. 로컬에서는 멀쩡했고 배포 후 요청이 `localhost`로 나가면서 드러났습니다. 런타임 주입이 정적 빌드 산출물에 안 먹는 게 원인이라 빌드 인자로 바꾸고, 같은 문제가 웹소켓 주소에서 재발하자 트러블슈팅 문서로 남겼습니다.

> 쿠폰 프로젝트에서는 1단계 동시성 테스트가 2 · 3단계로 복사돼 있었습니다. Redis 초기화가 빠져 전부 탈락하는 상태였고, 예외를 세지 않아 출력이 "성공 100 · 실패 0"으로 찍혀 나머지 900건이 사라져 보였습니다. `성공 + 탈락 == 1000` 단언을 넣어 삼켜진 예외가 없는지부터 확인하게 고쳤습니다.

**실제 사용량**

아래는 로컬 세션 기록을 집계한 것입니다. 쓰는 쪽에 토큰이 몰리고 검토는 적은 횟수로 도는데, 되돌린 판단은 대부분 그 적은 쪽에서 나왔습니다.

<div align="center">
  <img src="https://raw.githubusercontent.com/joejaeyoung/joejaeyoung/main/ai-usage.svg" alt="AI pair usage" width="860" />
</div>

<sub>최근 30일 롤링 집계이고, 각 블록에 전체 기간 누적도 함께 적었습니다. 매일 아침 8시에 로컬 launchd가 다시 돌려 갱신합니다. 집계는 <a href="gen_ai_usage.py"><code>gen_ai_usage.py</code></a>, 갱신은 <a href="update-ai-usage.sh"><code>update-ai-usage.sh</code></a>에 있습니다. 비용은 공개 API 단가로 환산한 추정치입니다.</sub>

<br />

## 📈 활동

<div align="center">
  <img src="https://ghchart.rshah.org/1f6feb/joejaeyoung" alt="contributions" width="780" />
</div>

<div align="center">
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=joejaeyoung&theme=github_dark" height="180" />
  <img src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=joejaeyoung&theme=github_dark" height="180" />
</div>

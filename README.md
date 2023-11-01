# 👩🏻‍💻 크레드잇 파이썬 과제

## ✏️ 주요 목표
- 면접 떄 질문 주셨던 patch 사용해보기 (-> ProjectEditorDetail에 사용)
- 면접 때 질문 주셨던 Custom Authentication 사용해보기 (-> JWT Authentication 완료)
- S3로 사진 파일 업로드하기
- testcode 작성하기
- 프로젝트 신청시 관리자 처리를 검토중/승인/미승인 으로 나눠서 각각 적용하기

## 📝 구성
- Custom User : AbstractUser로 구현. is_staff로 스태프/일반 회원 구분.
- Project 신청 : 유저가 project를 신청(post)하면 -> admin의 프로젝트 리스트에 해당 프로젝트가 올라감 -> 관리자는 adminpage/under-review 에서 검토중 프로젝트를 모아 볼 수 있음
- Project 승인 : project 승인시(project-editor/pk 에 is_approved 를 approval로 patch) 해당 project는 api/v1/projects에 공개됨
- Project 미승인 : project 미승인시(project-editor/pk 에 is_approved 를 disapproval로 patch) 해당 project는 공개되지 않음.
- User의 me/projects 페이지 : 본인이 신청한 모든 project 목록을 볼 수 있음. 승인/미승인/검토중 상태 확인 가능
- Adminpage : 전체 프로젝트 리스트와, 처리가 필요한 검토중 프로젝트 리스트를 볼 수 있음
- Projects : 승인된 프로젝트들을 볼 수 있음
- 유저 페이지 : 해당 유저가 작성한 승인된 프로젝트들을 모아 볼 수 있음
- OAuth : kakao 로그인 가능

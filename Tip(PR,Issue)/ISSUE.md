# [[Intro\] ONE-vscode 컨트리뷰션 가이드 (기초)]



### 이다영 멘토님 

#### Intro

ONE-vscode 레포지토리에 컨트리뷰션하게되신 것을 환영합니다. 오늘 미팅에서 많이 질문을 주셨는데, 제가 처음 입사해서 파트에 들어왔을때도 이런것들을 처음 알아야 했던게 생각나더라구요.조만간에 다들 첫 Issue와 PR을 만드시면서 궁금한게 많으실 텐데요, 간단하게 설명드리겠습니다.

#### 커뮤니티 가이드라인

아래와 같이, 레포지토리 위키에 저희 파트의 커뮤니티 가이드라인과 Governance가 적혀져있습니다.

https://github.com/Samsung/ONE-vscode/wiki/Community-Guidelines

 https://github.com/Samsung/ONE-vscode/wiki/Governance

#### 라이센스

https://github.com/Samsung/ONE-vscode/wiki/License

Apache 2.0을 사용합니다.혹시 개발중에 외부 npm 모듈을 사용하시게 될 시에, Dependency를 확인하셔야 하는데요, MIT 라이센스나 Apache2.0 라이센스를 사용하면 괜찮지만 GPL계열 라이센스는 '사용하는 코드는 반드시 전문 공개해야 한다'는 강력한 공개원칙을 준수하기 때문에, 사용하지 않도록 하고있습니다.

#### Issue

Issue 제목은 보통 `[모듈이름] 이슈 제목` 형식으로 만듭니다. 만약 속하는 모듈이 없는 General한 이슈이면 대괄호 부분을 생략하고 `이슈 제목` 만 적습니다.적당한 label (Question/Help wanted)을 달면 좋습니다.

#### Commit

커밋 메세지는 아래와 같이 제목/본문/Sign-off 로 나뉘어집니다.

```
[lint] Remove no-prototype-builtins <--- 커밋메세지 This commit adds "no-prototype-builtins" rule and fixes errors accordingly.                <--------------커밋 본문 ONE-vscode-DCO-1.0-Signed-off-by: dayo09 <dayoung.lee@samsung.com>  <----- Sign-off
```

커밋 메세지는 위 형식대로 1개만 만들면 됩니다. PR당 커밋을 여러개 포함할 경우에, 첫 커밋 메세지 외에는 1 line으로 짧게 적으시면 됩니다. (나중에 squash merge 합니다.)

#### 제목

제목의 경우 Issue와 같이 `[모듈이름] Commit 제목` 형식으로 만듭니다. 만약 속하는 모듈이 없는 General한 이슈이면 대괄호 부분을 생략하고 `Commit 제목` 만 적습니다.

#### 본문

커밋 본문은 해당 커밋에 대한 설명을 적습니다.

#### Sign-off

Sign-off 라인입니다. 저희 DCO(Developer's Certificate of Origin)를 읽고 이에 동의하는 서명을 남긴다는 의미인데요, 이 싸인이 있어야 코드를 머지할 수 있습니다. DCO의 의미와 자동 hook 만드는 법 등에 대한 설명은 아래를 참고하세요.

 https://github.com/Samsung/ONE-vscode/wiki/ONE-vscode-Developer's-Certificate-of-Origin

#### PR

origin의 commit을 Samsung/ONE 레포에 push하기 위하여 pull request를 만듭니다. https://github.com/Samsung/ONE-vscode/pulls본인의 계정의 origin에 origin/main에 없는 새로운 커밋을 포함한 branch가 있다면 pulls에서 PR을 만들 수 있습니다.가장 위에 있는 커밋 기준으로 메세지를 적어주세요. (커밋이 1개라면 자동으로 채워짐)Merge 기준은 approval 2개입니다. (타이포 등 아주 간단한 fix는 approval 1개)

## 남궁석 멘토님

정리 감사합니다 👍 👍 다만 아래 내용도 추가해주시면 감사하겠습니다 ㅎㅎ

(라이센스 관련 주의사항 내용추가) 

개발을 하시다보면 다른 오픈소스 참고하여 코드를 작성하시는 경우가 종종 발생합니다. 이러한 경우 반드시 출처를 주석 등으로 명시해주셔야 하며, 참고하시는 오픈소스의 라이센스 역시 npm package와 마찬가지의 이유로 GPL등의 라이센스를 갖는 소스코드는 참고하실 수 없습니다.

(Commit - 본문 내용추가)

 본문을 작성하지 않을 경우 머지가 불가능하므로 꼭 작성해주셔야 합니다. 또한 commit에는 링크가 포함되지 않도록 해주시기 바랍니다. 링크가 포함될 경우, PR에 업데이트가 일어날 때마다 해당 링크에 불필요한 notification이 발생할 수 있기 때문입니다.

(PR 내용추가) 

단, upstream인 https://github.com/Samsung/ONE-vscode에 있는 main, release 브랜치에는 **절대** push를 해서는 안되므로 실수가 발생하지 않도록 반드시 주의 부탁드립니다. 해당 브랜치들의 commit들은 Pull Request를 통해 형상관리가 되어야 하며 이 브랜치들에 사고가 발생할 경우... 너무나도 슬퍼집니다...👍8 
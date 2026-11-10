# Hand Tracking - 손 제스처로 마우스 제어

웹캠으로 손을 인식하고, 손가락 제스처로 마우스 동작을 자동 제어하는 프로젝트입니다.

## 기능

### 손가락 제스처 인식
| 제스처 | 기능 |
|--------|------|
| **검지만 펴짐** | 마우스 이동 |
| **주먹 쥐기** | 마우스 드래그 (지속) |
| **검지+중지 끝 접촉** | 좌클릭 |
| **엄지+검지+중지 펴짐** | 우클릭 |
| **검지+중지+약지+소지 펴짐** | 스크롤 업 |
| **중지+약지+소지 펴짐** | 스크롤 다운 |
| **5손가락 전부 펴짐** | 마우스 고정 |

## 요구 사항

- **Python 3.11** (정확히 3.11 — `mediapipe 0.10.9`가 3.12 이상을 지원하지 않음)
- 웹캠
- 지원 OS: Windows (x64), macOS (Apple Silicon: **13 이상**, Intel: **14 이상**), Linux (x64 / ARM64, **X11 데스크톱**)
  - macOS 버전이 이보다 낮으면 OpenCV 설치 파일이 없어 설치가 실패합니다
  - Windows ARM, Linux Wayland 환경은 지원되지 않습니다

## 설치 및 실행 (권장: uv)

[uv](https://docs.astral.sh/uv/)를 쓰면 Python 3.11 설치부터 의존성까지 자동으로 맞춰집니다.

```bash
git clone https://github.com/lkw-k/HandTracking.git
cd HandTracking

uv sync          # Python 3.11 + 의존성 자동 설치 (uv.lock 기준)
uv run main.py   # 실행
```

uv 설치: macOS/Linux `curl -LsSf https://astral.sh/uv/install.sh | sh`, Windows `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

> **업데이트 후 `module 'cv2' has no attribute ...` 에러가 나면**
> 예전 버전은 `opencv-python`과 `opencv-contrib-python`이 함께 설치돼 있었는데, 업데이트로 하나가 제거되면서 공유 파일이 같이 지워진 것입니다. 아래 명령으로 복구하세요.
> ```bash
> uv sync --reinstall-package opencv-contrib-python
> ```
> (pip 사용 시: `pip uninstall -y opencv-python opencv-contrib-python && pip install opencv-contrib-python`)

### pip로 설치하는 경우

반드시 **Python 3.11**로 가상환경을 만들어야 합니다.

```bash
python3.11 -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install "mediapipe==0.10.9" opencv-contrib-python "pyautogui>=0.9.54"
python main.py
```

### 주요 라이브러리
- **mediapipe (0.10.9)**: 손 인식 및 랜드마크 감지
- **opencv-contrib-python**: 웹캠 영상 처리 및 시각화 (mediapipe가 요구하는 패키지와 통일)
- **pyautogui**: 마우스/키보드 제어

## OS별 필수 설정

### macOS
처음 실행하면 권한 요청이 뜹니다. 거부했거나 동작하지 않으면
**시스템 설정 → 개인정보 보호 및 보안**에서 실행한 터미널 앱(Terminal, iTerm, VS Code 등)에 아래 권한을 허용한 뒤 터미널을 재시작하세요.
- **카메라**: 없으면 웹캠 창이 뜨지 않음
- **손쉬운 사용**: 없으면 마우스가 움직이지 않음

### Windows
- 설정 → 개인정보 → 카메라에서 데스크톱 앱의 카메라 접근 허용

### Linux
- X11 세션에서 실행해야 합니다 (Wayland에서는 pyautogui가 마우스를 제어하지 못함)
- 웹캠 권한: 사용자가 `video` 그룹에 속해야 할 수 있음 (`sudo usermod -aG video $USER`)
- 시스템 Python을 쓰는 경우 tkinter가 필요합니다. 없으면 시작 즉시 `You must install tkinter` 메시지와 함께 종료됩니다 (`sudo apt install python3-tk`). uv는 시스템에 Python 3.11이 있으면 그것을 쓰므로 uv 사용자도 해당될 수 있습니다 (`uv sync --managed-python`으로 uv 전용 Python을 쓰면 tkinter 포함)

## 사용 방법

1. 웹캠 창("Hand Image")이 열립니다
2. 손을 카메라에 보여줍니다
3. 손가락 제스처로 마우스를 제어합니다

### 종료 방법
- 웹캠 창을 클릭해 활성화한 뒤 **`p`** 키 (한글 입력 상태면 영문으로 전환 후 입력)
- 또는 실행한 터미널에서 **`Ctrl + C`**
- 비상시: 마우스를 **화면 왼쪽 위 모서리**로 이동하면 pyautogui 안전장치가 프로그램을 중단합니다
- 드래그 중 강제 종료해 마우스 버튼이 눌린 상태로 남으면 마우스를 한 번 클릭하세요

## 주요 파라미터

- **해상도**: 320x240 (낮은 해상도로 성능 최적화)
- **프레임 레이트**: 120 FPS
- **마우스 스무딩**: 0.23 (마우스 움직임을 부드럽게 함)

## 알려진 제한사항

- 한 손만 인식 (최대 1개 손)
- 충분한 조명이 필요합니다
- 손이 카메라 범위를 벗어나면 드래그 자동 해제
- 웹캠이 여러 개면 첫 번째 장치(0번)를 사용합니다

## 개발 계획

- [ ] 양손 동시 인식 지원
- [ ] 커스텀 제스처 추가
- [ ] 마우스 속도/민감도 조절 UI
- [ ] 제스처 감도 튜닝 옵션

## 라이센스

MIT

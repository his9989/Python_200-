# pygame : 파이썬 확장 모듈. 파이썬으로 게임을 구현하는 라이브러리
import pygame
import random
from time import sleep

# 게임에 사용되는 전역 변수
BLACK = (0,0,0)     # 검은색 rgb 변수 선언. 흰색은 (255, 255, 255)
RED = (255,0,0)     # 빨간색 rgb 변수 선언.
pad_width = 480     # 게임 화면 너비 변수 선언
pad_height = 640    # 게임 화면 높이 변수 선언
fighter_width = 36  # 전투기 이미지의 가로 변수 선언
fighter_height = 38 # 전투기 이미지의 세로 변수 선언
enemy_width = 26    # 적 이미지의 가로 변수 선언
enemy_height = 20   # 적 이미지의 세로 변수 선언

# 적을 맞춘 갯수 출력
def drawScore(count):
    # 게임 화면 객체 선언
    global gamepad
    # 갯수 출력하기 위한 font 설정
    font = pygame.font.SysFont(None, 20)
    # 출력하고자 하는 text 설정
    text = font.render('Enemy Kills : ' + str(count), True, (255, 255, 255))
    # text 출력
    gamepad.blit(text, (0,0))

# 적이 통과한 갯수 출력
def drawPassed(count):
    global gamepad
    font = pygame.font.SysFont(None, 20)
    text = font.render('Enemy Passed: ' + str(count), True, RED)
    gamepad.blit(text, (360, 0))

# 충돌 시 crash, 3번 적이 지나갈 시 Game Over!를 출력
def dispMessage(text):
    global gamepad
    # 기본 font 설정
    textfont = pygame.font.Font('freesansbold.ttf', 80)
    # text color 설정
    text = textfont.render(text, True, RED)
    textpos = text.get_rect()
    textpos.center = (pad_width/2, pad_height/2)
    gamepad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    # 게임 재 시작 호출
    runGame()

# 전투기가 적과 충돌했을 때 메시지 출력
def crash():
    global gamepad
    dispMessage('Crashed!')

# 게임 오버 메시지 보이기
def gameover():
    global gamepad
    dispMessage('Game Over')

# 게임에 등장하는 객체를 드로잉
# 0, 0 : 왼쪽 상단 모서리 좌표
# pad_width, pad_height : 오른쪽 하단 모서리 좌표
def drawObject(obj, x, y):
    global gamepad              # gamepad 객체 선언 (게임의 바탕 화면)
    gamepad.blit(obj, (x, y))   # obj를 화면에 그리는 실제 함수

# 게임 실행 메인 함수
def runGame():
    # gamepad : 게임이 진행되는 화면
    # clock : 게임의 초당 프레임 설정 (FPS). pygame이 제공하는 Clock 객체
    global gamepad, clock, fighter, enemy, bullet

    # 미사일에 적이 맞았을 경우 True로 설정하는 Boolean Flag
    isShot = False
    
    # showcount와 enemy_passed 초기화
    shotcount = 0
    enemy_passed = 0
    
    # 무기 좌표를 저장하는 리스트
    bullet_xy = []

    # 전투기 초기 위치(x, y) 설정
    x = pad_width*0.45
    y = pad_height*0.9
    x_change = 0        # 전투기의 좌, 우 이동 거리 변수

    # 적 초기 위치 설정
    # 적은 단순하게 내려가기만 한다.
    enemy_x = random.randrange(0, pad_width-enemy_width)
    enemy_y = 0
    enemy_speed = 3

    # x를 클릭하고 빠져나오도록 확인하는 boolean 변수
    ongame = False
    
    while not ongame:
        # pygame.event.get() : 게임에서 발생하는 이벤트 return.
        for event in pygame.event.get():
            # pygame.QUIT는 마우스로 창을 닫는 이벤트.
            # 즉, event.type이 마우스로 창을 닫는 이벤트인 경우, ongame을 False로 설정하여 while을 바쪄나온다.
            if event.type == pygame.QUIT:
                ongame = True

            # pygame.KEYDOWN : 키보드가 눌러졌을 때 발생하는 이벤트 타입
            if event.type == pygame.KEYDOWN:
                # 왼쪽 : K_LEFT, 오른쪽 : K_RIGHT
                if event.key == pygame.K_LEFT :
                    x_change -= 5

                elif event.key == pygame.K_RIGHT:
                    x_change += 5

                # Left CTRL가 클릭되는 경우
                elif event.key == pygame.K_LCTRL:
                    # 게임 화면 상에 2개의 미사일만 출력될 수 있다.
                    if len(bullet_xy)<2:
                        bullet_x = x + fighter_width/2          # 미사일의 초기 x 좌표 설정
                        bullet_y = y - fighter_height           # 미사일의 초기 y 좌표 설정
                        bullet_xy.append([bullet_x, bullet_y])  # 미사일 좌표 저장

            # pygame.KEYUP : 누르고 있던 키보드가 떼졌을 때 발생하는 이벤트 타입
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0    # x_change를 0으로 초기화

        gamepad.fill(BLACK)         # 게임 화면을 검은색으로 채운다.

        # 전투기의 위치 변경
        x += x_change
        # 단, 화면의 범위 내에서만 움직일 수 있다.
        if x<0:
            x=0
        elif x>pad_width - fighter_width:
            x = pad_width - fighter_width

        # 전투기가 적과 충돌했는지 체크
        if y < enemy_y + enemy_height:
            if(enemy_x > x and enemy_x < x+fighter_width) or (enemy_x + enemy_width >x and enemy_x + enemy_width <x + fighter_width):
                crash()

        # 게임 화면 위에 전투기를 표시하는 코드
        drawObject(fighter, x, y)

        # 게임 화면 위에 미사일을 표시하는 코드
        if len(bullet_xy) !=0:
            for i, bxy in enumerate(bullet_xy):
                # 미사일의 y 좌표 값을 10만큼 감소. 즉, 10의 속도로 위로 올라가게 한다.
                bxy[1] -= 10
                bullet_xy[i][1] = bxy[1]

                if bxy[1] < enemy_y :
                    if bxy[0] > enemy_x and bxy[0] < enemy_x + enemy_width :
                        bullet_xy.remove(bxy)
                        isShot = True
                        shotcount+=1

                # 미사일이 게임 화면 밖으로 나가면 삭제한다.
                if bxy[1] <=0:
                    try:
                        bullet_xy.remove(bxy)
                    except:
                        pass

        if len(bullet_xy) != 0:
            for bx, by in bullet_xy:
                drawObject(bullet, bx, by)

        # shotcount 출력
        drawScore(shotcount)

        # 적이 일정한 속도로 내려가도록 하는 코드
        enemy_y += enemy_speed
        if enemy_y > pad_height:
            enemy_y = 0
            enemy_x = random.randrange(0, pad_width- enemy_width)
            enemy_passed +=1

        if enemy_passed == 3:
            gameover()

        drawPassed(enemy_passed)

        if isShot:
            enemy_speed += 1
            if enemy_speed >= 10:
                enemy_speed = 10
            enemy_x = random.randrange(0, pad_width - enemy_width)
            enemy_y = 0
            isShot = False

        # 게임 화면 위에 적을 표시하는 코드
        drawObject(enemy, enemy_x, enemy_y)

        pygame.display.update()     # 게임 화면을 다시 그린다. 즉, 게임 화면 업데이트
        clock.tick(60)              # FPS : 60으로 설정. 사람 눈에 자연스러운 값은 30이다.

    pygame.quit()                   # 초기화한 pygame을 종료한다.

# 게임 초기화 함수
def initGame():
    global gamepad, clock, fighter, enemy, bullet

    pygame.init()                   # pygame 라이브러리를 초기화. 즉, pygame을 활용할 때 마다, pygame 라이브러리를 초기화 해줘야 한다.
    gamepad = pygame.display.set_mode((pad_width, pad_height))
                                    # 게임 화면의 크기 설정
    pygame.display.set_caption('MyGalaga')
                                    # 게임 화면의 타이틀 바의 이름 설정
    fighter = pygame.image.load('fighter.png')      # 전투기 이미지
    enemy = pygame.image.load('enemy.png')          # 적 이미지
    bullet = pygame.image.load('bullet.png')        # 미사일 이미지
    clock = pygame.time.Clock()     # Clock 객체 생성

initGame()
runGame()

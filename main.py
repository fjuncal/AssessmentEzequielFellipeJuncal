import requests
import pygame, sys
import io
from bs4 import BeautifulSoup



def pegarUsuario(usuario):


    response = requests.get(f'https://github.com/{usuario}')
    responseRepositorio = requests.get(f'https://github.com/{usuario}?tab=repositories')
    if response:
        texto = response.text
        soup = BeautifulSoup(texto, 'html.parser')

        textoRepositorio = responseRepositorio.text
        soupRepositorio = BeautifulSoup(textoRepositorio, 'html.parser')

        nomeUsuario = soup.find('span', class_='p-name')
        apelidoUsuario = soup.find('span', class_='p-nickname')
        fotoUsuario = soup.find('img', class_='avatar-user')
        infoUsuario = soup.find('div', class_='user-profile-bio')

        usuarioDict = {
            'nome': nomeUsuario.text,
            'apelido': apelidoUsuario.text,
            'foto': fotoUsuario['src'],
            'informacao': infoUsuario.text,
            'repositorio': [],
        }
        # print(estrelaUser)

        for i in soupRepositorio.find_all('h3'):
            usuarioDict['repositorio'].append(i.text.strip().replace('\n', ''))


        usuarioDict['repositorio'].pop(0)


        return usuarioDict
    else:
        return print('usuario nao existe')


def main():
    pygame.init()
    pygame.display.set_caption("Git-Hub Profile")
    fotoTela = pygame.image.load('git.png')
    pygame.display.set_icon(fotoTela)

    largura_tela = 1000
    altura_tela = 600

    tela = pygame.display.set_mode((largura_tela, altura_tela))
    cor = (0, 0, 255)
    reat = pygame.Rect((40, 150, 50, 50))

    input_box = pygame.Rect(40, 500, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color((0,255,0))
    active = False
    color = color_inactive
    text = ''
    font = pygame.font.Font(None, 32)

    userInfoFonte = pygame.font.SysFont('Comic Sans MS', 20)
    nomeFonte = pygame.font.SysFont('arial', 20)

    posicao = 0
    inputUsuario = None

    terminou = False
    while not terminou:
        tela.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminou = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        inputUsuario = pegarUsuario(text)
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                if event.key == pygame.K_RIGHT:
                    posicao+=1
                if event.key == pygame.K_LEFT:
                    if posicao < 0:
                        posicao = len(inputUsuario['repositorio'])
                    posicao-=1

        if inputUsuario:
            textoNome = nomeFonte.render('Nome: ' + inputUsuario['nome'], False, (255, 255, 255))
            tela.blit(textoNome, (200, 130))
            textoApelido = userInfoFonte.render('Apelido: '+ inputUsuario['apelido'],False, (255,255,255))
            tela.blit(textoApelido, (200, 180))
            if inputUsuario['informacao']:
                textoInformacao = userInfoFonte.render('Informações: ' + inputUsuario['informacao'], False, (255,255,255))
                tela.blit(textoInformacao, (200,230))
            r = requests.get(inputUsuario['foto'])
            img = io.BytesIO(r.content)
            perfil_img = pygame.image.load(img)
            tela.blit(perfil_img, reat)
            if posicao >= len(inputUsuario['repositorio']):
                posicao = 0
            textoRepositorio = userInfoFonte.render('Repositório: ' + inputUsuario['repositorio'][posicao], False, (255,255,255))
            tela.blit(textoRepositorio, (200, 280))

        txt_surface = font.render(text, True, color)
        width = max(100, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        tela.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(tela, color, input_box, 2)

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()

if __name__ == '__main__':
    main()




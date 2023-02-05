# First gets all keys, then checks if space has been pressed
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print('dwa')

    # Checks if there is a collision between the player and snail NOTE: This collision occurs multiple times as the game checks every frame if there is a collision. With some kind of heart system, you might want to give the player an invincibility frame to counter that
    # if player_rect.colliderect(snail_rect):
    #     print('coiidos')

    # Gets mouse position and checks if it is colliding with the player_rect
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint((mouse_pos)):
    #     print(pygame.mouse.get_pressed())

# Renders text
# score_surf = test_font.render("My game", False, (64 ,64, 64)).convert()
# score_rect = score_surf.get_rect(center = (400, 50))
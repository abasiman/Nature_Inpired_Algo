import pygame
import main
import sys
import genetics


def main_menu():
    WIDTH, HEIGHT = 1000, 800
    BACKGROUND_COLOR = (102, 153, 204)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Home Page for Nature Inspired Algorithms")

    # Font properties
    title_font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 24)

    # Size management variables
    title_size = (100, 60)
    button_size = (200, 60)

    # Title properties
   
    title_text = title_font.render("Nature Inspired Algorithms", True, (255, 215, 0))
    title_rect = pygame.Rect((WIDTH // 2 - title_size[0] // 2, title_size[1] // 2), title_size)
    title_text_rect = title_text.get_rect(center=title_rect.center)

    # ACO properties
    ACO_button = button_font.render("ACO", True, (255, 255, 255))
    button_rect = pygame.Rect(
        (WIDTH // 2 - button_size[0] // 2, HEIGHT // 2 - button_size[1] // 2), button_size)
    button_text_rect = ACO_button.get_rect(center=button_rect.center)

    # GENETICS PROPERTIES
    GEN_button = button_font.render("GENETICS", True, (255, 255, 255))
    gen_rect = pygame.Rect(
        (WIDTH // 2 - button_size[0] // 2, HEIGHT // 2 + 100 - button_size[1] // 2), button_size)
    gen_text_rect = GEN_button.get_rect(center=gen_rect.center)

    #ACO IMAGE
    
    aco_text = title_font.render(
        "ANT COLONY OPTIMIZATION", True, (255, 215, 0))
    aco_text_pos = pygame.Rect(
        (1260-WIDTH // 2 - title_size[0] // 2, 300 // 2), title_size)
    aco_text_img_rect = aco_text.get_rect(center=aco_text_pos.center)


    image_path = "aco.jpg"
    image = pygame.image.load(image_path)
    desired_width, desired_height = 300, 120
    resized_image = pygame.transform.scale(image, (desired_width, desired_height))

 
    image_x = (1500 - desired_width) // 2  
    image_y = (500 - desired_height) // 2  
    image_rect = resized_image.get_rect(topleft=(image_x, image_y))

    #GENETICS IMAGE
    gen_text = title_font.render("GENETICS ALGORITHMS", True, (255, 215, 0))
    gen_text_pos = pygame.Rect(
        (750-WIDTH // 2 - title_size[0] // 2, 300 // 2), title_size)
    gen_text_img_rect = gen_text.get_rect(center=gen_text_pos.center)

    gen_path = "gen.png"
    gen_image = pygame.image.load(gen_path)
    desired_width, desired_height = 300, 120
    resized_gen = pygame.transform.scale(
        gen_image, (desired_width, desired_height))

    gen_x = (500 - desired_width) // 2
    gen_y = (500 - desired_height) // 2
    gen_image_rect = resized_gen.get_rect(topleft=(gen_x, gen_y))



   
    
    # Main event loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    main.run_aco_simulation()
                elif gen_rect.collidepoint(event.pos):
                    genetics.main()

        screen.fill(BACKGROUND_COLOR)
        screen.blit(title_text, title_text_rect)
        screen.blit(gen_text, gen_text_img_rect)
        screen.blit(aco_text, aco_text_img_rect)
        
        # Draw the rectangles
        pygame.draw.rect(screen, (0, 128, 255), button_rect)
        pygame.draw.rect(screen, (0, 128, 255), gen_rect)

        # Draw the text
        screen.blit(ACO_button, button_text_rect)
        screen.blit(GEN_button, gen_text_rect)

        
        # Draw the resized image
        screen.blit(resized_image, image_rect)
        screen.blit(resized_gen, gen_image_rect)

        pygame.display.flip()


    pygame.quit()
    sys.exit()


# Call the main_menu function
if __name__ == "__main__":
    main_menu()

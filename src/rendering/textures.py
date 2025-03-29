from string import printable

import pygame
import zengl


def get_tex_array(surfs: list[pygame.Surface]) -> zengl.Image:
    ctx = zengl.context()
    size = surfs[0].get_size()
    texture = ctx.image(size, "rgba8unorm", array=len(surfs))
    for idx, surf in enumerate(surfs):
        texture.write(pygame.image.tobytes(surf, "RGBA", False), layer=idx)
    texture.mipmaps()
    return texture


def load_ttf_font(
    path: str, font_size: int
) -> tuple[list[pygame.Surface], dict[str, int]]:
    pygame.font.init()
    font = pygame.font.Font(path, font_size)
    surf_size = font.size("A")
    glyphs = []
    idx_map = {}

    for idx, char in enumerate(printable):
        surf = pygame.Surface(surf_size, pygame.SRCALPHA)
        surf.blit(font.render(char, True, (225, 255, 255)), (0, 0))
        glyphs.append(surf)
        idx_map[char] = idx

    return glyphs, idx_map


class Textures:
    def __init__(self) -> None:
        button_surf_1 = pygame.Surface((255, 255), pygame.SRCALPHA)
        button_surf_1.fill((255, 0, 0))
        button_surf_2 = pygame.Surface((255, 255), pygame.SRCALPHA)
        button_surf_2.fill((55, 155, 0))
        button_surf_3 = pygame.Surface((255, 255), pygame.SRCALPHA)
        button_surf_3.fill((55, 55, 55))
        surfs = [button_surf_1, button_surf_2, button_surf_3]
        for surf in surfs:
            pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 10)
        self.default_texture = get_tex_array(surfs)
        circuit_board_img_1 = pygame.image.load("src/assets/circuit_board.png")
        circuit_board_img_1.set_colorkey((0, 0, 0))
        circuit_board_img_2 = pygame.transform.flip(circuit_board_img_1, True, False)
        circuit_board_img_3 = pygame.transform.flip(circuit_board_img_1, False, True)
        circuit_board_img_4 = pygame.transform.flip(circuit_board_img_2, False, True)
        self.circuit_board_texture = get_tex_array(
            [
                circuit_board_img_1,
                circuit_board_img_2,
                circuit_board_img_3,
                circuit_board_img_4,
            ]
        )
        font_glyphs, self.font_idx_map = load_ttf_font(
            "src/assets/RobotoMono-Bold.ttf", 32
        )
        self.font_size = font_glyphs[0].get_size()
        self.font_texture = get_tex_array(font_glyphs)
        ui_panel_img = pygame.Surface((255, 255), pygame.SRCALPHA)
        pygame.draw.rect(ui_panel_img, (0, 0, 0, 200), ui_panel_img.get_rect())
        self.ui_panel_texture = get_tex_array([ui_panel_img])

        robot_img = pygame.image.load("src/assets/robot.png")
        robot_img_scaled = pygame.transform.scale_by(robot_img, 2.5)
        robot_img_scaled.set_colorkey((255, 255, 255))
        self.robot_texture = get_tex_array([robot_img_scaled])
        self.robot_img_size = robot_img_scaled.get_size()

        obstacle_img_paths = [
            "src/assets/obstacle_1.png",
            "src/assets/obstacle_2.png",
            "src/assets/obstacle_3.png",
            "src/assets/obstacle_4.png",
            "src/assets/obstacle_5.png",
            "src/assets/obstacle_6.png",
            "src/assets/obstacle_7.png",
        ]
        self.obstacle_sizes = {}
        self.obstacle_textures = {}
        for idx, img_path in enumerate(obstacle_img_paths):
            surf = pygame.image.load(img_path)
            surf = pygame.transform.scale_by(surf, 0.5)
            surf.set_colorkey((255, 255, 255))
            self.obstacle_textures.update(
                {f"obstacle_texture_{idx}": get_tex_array([surf])}
            )
            self.obstacle_sizes.update({f"obstacle_texture_{idx}": surf.get_size()})

        self.intro_panel_texture, self.intro_panel_size = (
            self.create_intro_panel_texture()
        )

    @staticmethod
    def create_intro_panel_texture() -> tuple[zengl.Image, tuple[int, int]]:
        surf = pygame.Surface((1400, 600), pygame.SRCALPHA)
        pygame.draw.rect(surf, (0, 0, 0, 200), surf.get_rect())
        text = (
            "\n"
            "                           DATASTREAM DEFENDER!\n\n"
            "       * Defend the datastream from the incoming obstacles!\n"
            "       * Use ARROW KEYS to move and press/hold SPACE to shoot\n"
            "       * You can shoot down the obstacles to gain money\n"
            "       * Use the money to buy health and upgrades (press F)\n"
            "       * Shooting also costs a small amount of money\n"
            "       * You'll lose health if you collide with an enemy\n"
            "       * You'll also lose health when enemies reach the top\n"
            "       ** Hint: Don't forget to get upgrades and health!\n\n"
            "                       Press SPACE to start the game\n"
        )
        font = pygame.font.Font("src/assets/RobotoMono-Bold.ttf", 32)
        text_surf = font.render(text, True, (255, 255, 255))
        surf.blit(text_surf, (10, 10))
        return get_tex_array([surf]), surf.get_size()

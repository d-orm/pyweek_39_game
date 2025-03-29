from enum import StrEnum

import pygame


class Inputs(StrEnum):
    Mouse1 = "mouse1"
    Mouse2 = "mouse2"
    Mouse3 = "mouse3"
    Mouse4 = "mouse4"
    Mouse5 = "mouse5"
    Tab = "tab"
    ArrowLeft = "left_arrow"
    ArrowRight = "right_arrow"
    ArrowUp = "up_arrow"
    ArrowDown = "down_arrow"
    PageUp = "page_up"
    PageDown = "page_down"
    Home = "home"
    End = "end"
    Insert = "insert"
    Delete = "delete"
    Backspace = "backspace"
    Space = "space"
    Enter = "enter"
    Escape = "escape"
    Quote = "apostrophe"
    Comma = "comma"
    Minus = "minus"
    Period = "period"
    Slash = "slash"
    Semicolon = "semicolon"
    Equal = "equal"
    BracketLeft = "left_bracket"
    Backslash = "backslash"
    BracketRight = "right_bracket"
    Backquote = "grave_accent"
    CapsLock = "caps_lock"
    ScrollLock = "scroll_lock"
    NumLock = "num_lock"
    PrintScreen = "print_screen"
    Pause = "pause"
    Numpad0 = "keypad_0"
    Numpad1 = "keypad_1"
    Numpad2 = "keypad_2"
    Numpad3 = "keypad_3"
    Numpad4 = "keypad_4"
    Numpad5 = "keypad_5"
    Numpad6 = "keypad_6"
    Numpad7 = "keypad_7"
    Numpad8 = "keypad_8"
    Numpad9 = "keypad_9"
    NumpadDecimal = "keypad_decimal"
    NumpadDivide = "keypad_divide"
    NumpadMultiply = "keypad_multiply"
    NumpadSubtract = "keypad_subtract"
    NumpadAdd = "keypad_add"
    ShiftLeft = "left_shift"
    ControlLeft = "left_ctrl"
    AltLeft = "left_alt"
    MetaLeft = "left_super"
    ShiftRight = "right_shift"
    ControlRight = "right_ctrl"
    AltRight = "right_alt"
    MetaRight = "right_super"
    Menu = "menu"
    Digit0 = "0"
    Digit1 = "1"
    Digit2 = "2"
    Digit3 = "3"
    Digit4 = "4"
    Digit5 = "5"
    Digit6 = "6"
    Digit7 = "7"
    Digit8 = "8"
    Digit9 = "9"
    KeyA = "a"
    KeyB = "b"
    KeyC = "c"
    KeyD = "d"
    KeyE = "e"
    KeyF = "f"
    KeyG = "g"
    KeyH = "h"
    KeyI = "i"
    KeyJ = "j"
    KeyK = "k"
    KeyL = "l"
    KeyM = "m"
    KeyN = "n"
    KeyO = "o"
    KeyP = "p"
    KeyQ = "q"
    KeyR = "r"
    KeyS = "s"
    KeyT = "t"
    KeyU = "u"
    KeyV = "v"
    KeyW = "w"
    KeyX = "x"
    KeyY = "y"
    KeyZ = "z"
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    F4 = "f4"
    F5 = "f5"
    F6 = "f6"
    F7 = "f7"
    F8 = "f8"
    F9 = "f9"
    F10 = "f10"
    F11 = "f11"
    F12 = "f12"
    F13 = "f13"
    F14 = "f14"
    F15 = "f15"
    F16 = "f16"
    F17 = "f17"
    F18 = "f18"
    F19 = "f19"
    F20 = "f20"
    F21 = "f21"
    F22 = "f22"
    F23 = "f23"
    F24 = "f24"


PygameMouseButtons = [0, 1, 2, 3, 4, 5]

PygameKeyMap: dict[Inputs, int] = {
    Inputs.Mouse1: 0,
    Inputs.Mouse2: 2,
    Inputs.Mouse3: 1,
    Inputs.Mouse4: 3,
    Inputs.Mouse5: 4,
    Inputs.Tab: pygame.K_TAB,
    Inputs.ArrowLeft: pygame.K_LEFT,
    Inputs.ArrowRight: pygame.K_RIGHT,
    Inputs.ArrowUp: pygame.K_UP,
    Inputs.ArrowDown: pygame.K_DOWN,
    Inputs.PageUp: pygame.K_PAGEUP,
    Inputs.PageDown: pygame.K_PAGEDOWN,
    Inputs.Home: pygame.K_HOME,
    Inputs.End: pygame.K_END,
    Inputs.Insert: pygame.K_INSERT,
    Inputs.Delete: pygame.K_DELETE,
    Inputs.Backspace: pygame.K_BACKSPACE,
    Inputs.Space: pygame.K_SPACE,
    Inputs.Enter: pygame.K_RETURN,
    Inputs.Escape: pygame.K_ESCAPE,
    Inputs.Quote: pygame.K_QUOTE,
    Inputs.Comma: pygame.K_COMMA,
    Inputs.Minus: pygame.K_MINUS,
    Inputs.Period: pygame.K_PERIOD,
    Inputs.Slash: pygame.K_SLASH,
    Inputs.Semicolon: pygame.K_SEMICOLON,
    Inputs.Equal: pygame.K_EQUALS,
    Inputs.BracketLeft: pygame.K_LEFTBRACKET,
    Inputs.Backslash: pygame.K_BACKSLASH,
    Inputs.BracketRight: pygame.K_RIGHTBRACKET,
    Inputs.Backquote: pygame.K_BACKQUOTE,
    Inputs.CapsLock: pygame.K_CAPSLOCK,
    Inputs.ScrollLock: pygame.K_SCROLLOCK,
    Inputs.NumLock: pygame.K_NUMLOCK,
    Inputs.PrintScreen: pygame.K_PRINTSCREEN,
    Inputs.Pause: pygame.K_PAUSE,
    Inputs.Numpad0: pygame.K_KP_0,
    Inputs.Numpad1: pygame.K_KP_1,
    Inputs.Numpad2: pygame.K_KP_2,
    Inputs.Numpad3: pygame.K_KP_3,
    Inputs.Numpad4: pygame.K_KP_4,
    Inputs.Numpad5: pygame.K_KP_5,
    Inputs.Numpad6: pygame.K_KP_6,
    Inputs.Numpad7: pygame.K_KP_7,
    Inputs.Numpad8: pygame.K_KP_8,
    Inputs.Numpad9: pygame.K_KP_9,
    Inputs.NumpadDecimal: pygame.K_KP_PERIOD,
    Inputs.NumpadDivide: pygame.K_KP_DIVIDE,
    Inputs.NumpadMultiply: pygame.K_KP_MULTIPLY,
    Inputs.NumpadSubtract: pygame.K_KP_MINUS,
    Inputs.NumpadAdd: pygame.K_KP_PLUS,
    Inputs.ShiftLeft: pygame.K_LSHIFT,
    Inputs.ControlLeft: pygame.K_LCTRL,
    Inputs.AltLeft: pygame.K_LALT,
    Inputs.MetaLeft: pygame.K_LSUPER,
    Inputs.ShiftRight: pygame.K_RSHIFT,
    Inputs.ControlRight: pygame.K_RCTRL,
    Inputs.AltRight: pygame.K_RALT,
    Inputs.MetaRight: pygame.K_RSUPER,
    Inputs.Menu: pygame.K_MENU,
    Inputs.Digit0: pygame.K_0,
    Inputs.Digit1: pygame.K_1,
    Inputs.Digit2: pygame.K_2,
    Inputs.Digit3: pygame.K_3,
    Inputs.Digit4: pygame.K_4,
    Inputs.Digit5: pygame.K_5,
    Inputs.Digit6: pygame.K_6,
    Inputs.Digit7: pygame.K_7,
    Inputs.Digit8: pygame.K_8,
    Inputs.Digit9: pygame.K_9,
    Inputs.KeyA: pygame.K_a,
    Inputs.KeyB: pygame.K_b,
    Inputs.KeyC: pygame.K_c,
    Inputs.KeyD: pygame.K_d,
    Inputs.KeyE: pygame.K_e,
    Inputs.KeyF: pygame.K_f,
    Inputs.KeyG: pygame.K_g,
    Inputs.KeyH: pygame.K_h,
    Inputs.KeyI: pygame.K_i,
    Inputs.KeyJ: pygame.K_j,
    Inputs.KeyK: pygame.K_k,
    Inputs.KeyL: pygame.K_l,
    Inputs.KeyM: pygame.K_m,
    Inputs.KeyN: pygame.K_n,
    Inputs.KeyO: pygame.K_o,
    Inputs.KeyP: pygame.K_p,
    Inputs.KeyQ: pygame.K_q,
    Inputs.KeyR: pygame.K_r,
    Inputs.KeyS: pygame.K_s,
    Inputs.KeyT: pygame.K_t,
    Inputs.KeyU: pygame.K_u,
    Inputs.KeyV: pygame.K_v,
    Inputs.KeyW: pygame.K_w,
    Inputs.KeyX: pygame.K_x,
    Inputs.KeyY: pygame.K_y,
    Inputs.KeyZ: pygame.K_z,
    Inputs.F1: pygame.K_F1,
    Inputs.F2: pygame.K_F2,
    Inputs.F3: pygame.K_F3,
    Inputs.F4: pygame.K_F4,
    Inputs.F5: pygame.K_F5,
    Inputs.F6: pygame.K_F6,
    Inputs.F7: pygame.K_F7,
    Inputs.F8: pygame.K_F8,
    Inputs.F9: pygame.K_F9,
    Inputs.F10: pygame.K_F10,
    Inputs.F11: pygame.K_F11,
    Inputs.F12: pygame.K_F12,
    Inputs.F13: pygame.K_F13,
    Inputs.F14: pygame.K_F14,
    Inputs.F15: pygame.K_F15,
}

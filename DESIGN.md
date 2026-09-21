# Design notes

Reading this as: a product website for developers, with the PocketCPU app's compact native SwiftUI language, leaning toward a split-view workspace rather than an editorial landing page.

References: the included PocketCPU iPhone and iPad simulator captures, [Apple Terminal guide](https://support.apple.com/guide/terminal/welcome/mac), and [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/). The captures define the visual language. The external references inform accessibility and restrained system typography without copying product UI.

Tokens come directly from the app: paper `#f2f7fa`, ink `#0f2138`, separator `#c2d1db`, and signal teal `#006e78`. Dark mode uses app paper `#121c26`, ink `#e6f0f7`, separator `#3b4f5e`, and signal `#59c7cc`. Apple system fonts, compact 16px body text, quiet separators, and a 9px control radius follow the source interface. At 840px and wider, the site uses a persistent pale sidebar and white detail pane. Below that it becomes a compact navigation bar, like the app's compact navigation behavior. Screenshots carry all conversation and control detail; the site does not recreate a fake app.

The screenshots are actual iOS simulator captures. The visible sample labels must remain: these images demonstrate the development interface, not a live coding result. There are no external fonts, tracking scripts, or third-party assets. Design variance is 3, motion intensity is 1, and visual density is 6: the site is a readable public explanation built from the app's information hierarchy.

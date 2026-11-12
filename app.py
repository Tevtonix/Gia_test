import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from db import get_database_session
from repository import get_all_products_with_relations

FONT_NAME = "Arial"

COLOR_MAIN_BG = "#FFFFFF"
COLOR_SECONDARY_BG = "#6A5ACD"
COLOR_ACCENT_ACTION = "#4B0082"
COLOR_DISCOUNT_HIGHLIGHT = "#483D8B"
COLOR_OUT_OF_STOCK = "#808080"
COLOR_TEXT_DARK = "#000000"
COLOR_TEXT_LIGHT = "#FFFFFF"


def resolve_resource_path(file_name):
    if not file_name:
        return ""
    if os.path.exists(file_name):
        return file_name
    folder_path = os.path.join("resources", file_name)
    if os.path.exists(folder_path):
        return folder_path
    return ""


def generate_fallback_image(width, height, text_info):
    img = Image.new("RGB", (width, height), color="#DCDCDC")
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (width - 1, height - 1)], outline="#B0B0B0", width=2)
    draw.text((10, height // 2 - 8), text_info, fill="#505050")
    return img


def load_aspect_ratio_photo(image_file, dimensions=(140, 140)):
    loaded_image = None
    target_path = resolve_resource_path(image_file)

    if target_path:
        try:
            loaded_image = Image.open(target_path)
        except Exception:
            loaded_image = None

    if loaded_image is None:
        placeholder_path = resolve_resource_path("picture.png")
        if placeholder_path:
            try:
                loaded_image = Image.open(placeholder_path)
            except Exception:
                loaded_image = None

    if loaded_image is None:
        loaded_image = generate_fallback_image(
            dimensions[0], dimensions[1], "Нет фото"
        )

    # Масштабирование без искажения пропорций
    loaded_image.thumbnail(dimensions, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(loaded_image)


class BicycleStoreApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ООО «ВелосипедДрайв» — Каталог товаров")
        self.geometry("1060x760")
        self.minsize(860, 600)
        self.configure(bg=COLOR_MAIN_BG)

        self.rendered_images = []

        self.setup_window_icon()
        self.create_interface()
        self.refresh_catalog_data()

    def setup_window_icon(self):
        icon_path = resolve_resource_path("icon.ico")
        if icon_path:
            try:
                self.iconbitmap(icon_path)
                return
            except Exception:
                pass

        icon_png_path = resolve_resource_path("icon.png")
        if icon_png_path:
            try:
                tk_icon = tk.PhotoImage(file=icon_png_path)
                self.iconphoto(False, tk_icon)
            except Exception:
                pass

    def create_interface(self):
        # Панель заголовка (дополнительный фон #6A5ACD)
        self.header_panel = tk.Frame(
            self,
            bg=COLOR_SECONDARY_BG,
            height=85,
        )
        self.header_panel.pack(side=tk.TOP, fill=tk.X)
        self.header_panel.pack_propagate(False)

        # Размещение логотипа
        logo_path = resolve_resource_path("logo.png")
        raw_logo = None

        if logo_path:
            try:
                raw_logo = Image.open(logo_path)
                raw_logo.thumbnail((220, 65), Image.Resampling.LANCZOS)
                self.logo_tk = ImageTk.PhotoImage(raw_logo)
            except Exception:
                self.logo_tk = None
        else:
            self.logo_tk = None

        if self.logo_tk is None:
            raw_logo = generate_fallback_image(150, 50, "ВелосипедДрайв")
            self.logo_tk = ImageTk.PhotoImage(raw_logo)

        self.logo_widget = tk.Label(
            self.header_panel,
            image=self.logo_tk,
            bg=COLOR_SECONDARY_BG,
        )
        self.logo_widget.pack(side=tk.LEFT, padx=15, pady=10)

        self.header_label = tk.Label(
            self.header_panel,
            text="Каталог велосипедов и комплектующих",
            font=(FONT_NAME, 16, "bold"),
            bg=COLOR_SECONDARY_BG,
            fg=COLOR_TEXT_LIGHT,
        )
        self.header_label.pack(side=tk.LEFT, padx=10, pady=20)

        # Кнопка с акцентным цветом (#4B0082)
        self.btn_reload = tk.Button(
            self.header_panel,
            text="Обновить",
            font=(FONT_NAME, 11, "bold"),
            bg=COLOR_ACCENT_ACTION,
            fg=COLOR_TEXT_LIGHT,
            activebackground="#330055",
            activeforeground=COLOR_TEXT_LIGHT,
            relief=tk.FLAT,
            padx=18,
            pady=7,
            cursor="hand2",
            command=self.refresh_catalog_data,
        )
        self.btn_reload.pack(side=tk.RIGHT, padx=20, pady=20)

        # Контейнер списка товаров с прокруткой
        self.main_content = tk.Frame(self, bg=COLOR_MAIN_BG)
        self.main_content.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas_area = tk.Canvas(
            self.main_content,
            bg=COLOR_MAIN_BG,
            highlightthickness=0,
        )
        self.vertical_scroll = ttk.Scrollbar(
            self.main_content,
            orient=tk.VERTICAL,
            command=self.canvas_area.yview,
        )

        self.items_container = tk.Frame(self.canvas_area, bg=COLOR_MAIN_BG)
        self.items_container.bind(
            "<Configure>",
            lambda event: self.canvas_area.configure(
                scrollregion=self.canvas_area.bbox("all")
            ),
        )

        self.window_frame_id = self.canvas_area.create_window(
            (0, 0),
            window=self.items_container,
            anchor="nw",
        )

        self.canvas_area.bind(
            "<Configure>",
            lambda event: self.canvas_area.itemconfig(
                self.window_frame_id,
                width=event.width,
            ),
        )

        self.canvas_area.configure(yscrollcommand=self.vertical_scroll.set)
        self.vertical_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_area.bind_all(
            "<MouseWheel>",
            lambda event: self.canvas_area.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units",
            ),
        )

        # Статусная строка внизу
        self.status_bar = tk.Frame(
            self,
            bg=COLOR_MAIN_BG,
            height=30,
            relief=tk.RIDGE,
            bd=1,
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.info_counter = tk.Label(
            self.status_bar,
            text="",
            font=(FONT_NAME, 9),
            bg=COLOR_MAIN_BG,
            fg=COLOR_TEXT_DARK,
        )
        self.info_counter.pack(side=tk.LEFT, padx=12)

    def refresh_catalog_data(self):
        for widget in self.items_container.winfo_children():
            widget.destroy()

        self.rendered_images.clear()

        try:
            with get_database_session() as session:
                products_list = get_all_products_with_relations(session)
        except Exception as query_error:
            messagebox.showerror(
                "Ошибка подключения к PostgreSQL",
                f"Не удалось получить данные из БД:\n{query_error}\n\n"
                f"Убедитесь, что служба PostgreSQL запущена и пароль верен.",
            )
            return

        self.info_counter.config(
            text=f"Всего товаров в каталоге: {len(products_list)}"
        )

        for product in products_list:
            sku = product["sku"]
            product_name = product["product_name"]
            category_name = product["category_name"]
            description = product["description"]
            manufacturer_name = product["manufacturer_name"]
            supplier_name = product["supplier_name"]
            base_price = product["price"]
            unit_name = product["unit_name"]
            quantity = product["quantity_in_stock"]
            discount = product["discount"]
            photo_name = product["photo"]

            # ПРАВИЛО ПРИОРИТЕТА ВЫДЕЛЕНИЯ ЦВЕТОМ:
            # Если остаток 0 -> серый фон (#808080) имеет абсолютный приоритет!
            if quantity == 0:
                card_bg = COLOR_OUT_OF_STOCK
                card_fg = COLOR_TEXT_LIGHT
            elif discount > 15:
                card_bg = COLOR_DISCOUNT_HIGHLIGHT
                card_fg = COLOR_TEXT_LIGHT
            else:
                card_bg = COLOR_MAIN_BG
                card_fg = COLOR_TEXT_DARK

            card_border = "#CCCCCC" if card_bg == COLOR_MAIN_BG else card_bg

            card = tk.Frame(
                self.items_container,
                bg=card_bg,
                highlightbackground=card_border,
                highlightthickness=1,
                padx=14,
                pady=14,
            )
            card.pack(fill=tk.X, padx=16, pady=8, expand=True)

            # Область изображения
            photo_box = tk.Frame(
                card,
                bg=card_bg,
                width=140,
                height=140,
            )
            photo_box.pack(side=tk.LEFT, padx=(0, 16))
            photo_box.pack_propagate(False)

            photo_tk = load_aspect_ratio_photo(photo_name, dimensions=(140, 140))
            self.rendered_images.append(photo_tk)

            photo_label = tk.Label(photo_box, image=photo_tk, bg=card_bg)
            photo_label.pack(expand=True)

            # Область информации
            info_frame = tk.Frame(card, bg=card_bg)
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            title_lbl = tk.Label(
                info_frame,
                text=f"{product_name} (Арт. {sku})",
                font=(FONT_NAME, 12, "bold"),
                bg=card_bg,
                fg=card_fg,
                anchor="w",
                justify=tk.LEFT,
                wraplength=520,
            )
            title_lbl.pack(fill=tk.X)

            cat_lbl = tk.Label(
                info_frame,
                text=f"Категория: {category_name}",
                font=(FONT_NAME, 10, "italic"),
                bg=card_bg,
                fg=card_fg,
                anchor="w",
            )
            cat_lbl.pack(fill=tk.X, pady=(2, 4))

            safe_description = (
                description if description else "Описание отсутствует."
            )
            desc_lbl = tk.Label(
                info_frame,
                text=safe_description,
                font=(FONT_NAME, 9),
                bg=card_bg,
                fg=card_fg,
                anchor="w",
                justify=tk.LEFT,
                wraplength=520,
            )
            desc_lbl.pack(fill=tk.X, pady=(0, 6))

            partners_lbl = tk.Label(
                info_frame,
                text=f"Производитель: {manufacturer_name}  |  Поставщик: {supplier_name}",
                font=(FONT_NAME, 9),
                bg=card_bg,
                fg=card_fg,
                anchor="w",
            )
            partners_lbl.pack(fill=tk.X)

            stock_text = (
                f"На складе: {quantity} {unit_name}"
                if quantity > 0
                else "НЕТ В НАЛИЧИИ"
            )
            stock_color = (
                "#FFC0CB"
                if quantity == 0
                else (
                    card_fg if card_bg != COLOR_MAIN_BG else "#006400"
                )
            )

            stock_lbl = tk.Label(
                info_frame,
                text=stock_text,
                font=(FONT_NAME, 10, "bold"),
                bg=card_bg,
                fg=stock_color,
                anchor="w",
            )
            stock_lbl.pack(fill=tk.X, pady=(4, 0))

            # Область цен и скидок
            price_frame = tk.Frame(card, bg=card_bg, width=210)
            price_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

            discount_lbl = tk.Label(
                price_frame,
                text=f"Скидка: {discount}%",
                font=(FONT_NAME, 11, "bold"),
                bg=card_bg,
                fg="#FFEB3B"
                if card_bg != COLOR_MAIN_BG
                else COLOR_ACCENT_ACTION,
                anchor="e",
            )
            discount_lbl.pack(fill=tk.X, pady=(4, 4))

            # Расчет цены с действующей скидкой
            if discount > 0:
                final_price = base_price * (1.0 - (discount / 100.0))

                old_price_lbl = tk.Label(
                    price_frame,
                    text=f"Цена: {base_price:,.2f} ₽".replace(",", " "),
                    font=(FONT_NAME, 10),
                    bg=card_bg,
                    fg=card_fg,
                    anchor="e",
                )
                old_price_lbl.pack(fill=tk.X)

                final_price_lbl = tk.Label(
                    price_frame,
                    text=f"{final_price:,.2f} ₽".replace(",", " "),
                    font=(FONT_NAME, 14, "bold"),
                    bg=card_bg,
                    fg="#FF5252" if card_bg == COLOR_MAIN_BG else "#FFFFFF",
                    anchor="e",
                )
                final_price_lbl.pack(fill=tk.X)
            else:
                regular_price_lbl = tk.Label(
                    price_frame,
                    text=f"{base_price:,.2f} ₽".replace(",", " "),
                    font=(FONT_NAME, 13, "bold"),
                    bg=card_bg,
                    fg=card_fg,
                    anchor="e",
                )
                regular_price_lbl.pack(fill=tk.X, pady=(10, 0))


if __name__ == "__main__":
    app = BicycleStoreApp()
    app.mainloop()
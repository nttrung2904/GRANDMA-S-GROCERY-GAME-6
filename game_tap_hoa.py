import json
import os
import random
import tkinter as tk
from contextlib import redirect_stdout
from io import StringIO
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk


class CuaHangTapHoa:
    def __init__(self):
        self.so_tien = 500_000
        self.ngay_hien_tai = 1
        self.kho_hang = [
            {
                "ten": "Mì tôm",
                "gia_nhap": 3_000,
                "gia_ban": 5_000,
                "so_luong_ton": 50,
            },
            {
                "ten": "Kẹo mút",
                "gia_nhap": 1_000,
                "gia_ban": 2_000,
                "so_luong_ton": 100,
            },
            {
                "ten": "Cà phê đen",
                "gia_nhap": 8_000,
                "gia_ban": 12_000,
                "so_luong_ton": 30,
            },
            {
                "ten": "Nước mắm",
                "gia_nhap": 25_000,
                "gia_ban": 35_000,
                "so_luong_ton": 20,
            },
            {
                "ten": "Xà bông cục",
                "gia_nhap": 7_000,
                "gia_ban": 10_000,
                "so_luong_ton": 40,
            },
            {
                "ten": "Áo mưa",
                "gia_nhap": 15_000,
                "gia_ban": 25_000,
                "so_luong_ton": 15,
            },
            {
                "ten": "Nước đá",
                "gia_nhap": 5_000,
                "gia_ban": 10_000,
                "so_luong_ton": 30,
            },
            {
                "ten": "Bia/Mồi nhậu",
                "gia_nhap": 20_000,
                "gia_ban": 35_000,
                "so_luong_ton": 25,
            },
        ]
        self.so_ban_thieu = {}
        self.su_kien_hien_tai = None

    @staticmethod
    def dinh_dang_tien(so_tien):
        return f"{so_tien:,}".replace(",", ".") + " VND"

    def hien_thi_thong_ke(self):
        print("=" * 72)
        print("                 CUA HANG TAP HOA - THONG KE")
        print("=" * 72)
        print(f"So tien hien co : {self.dinh_dang_tien(self.so_tien)}")
        print(f"Ngay hien tai   : Ngay {self.ngay_hien_tai}")
        print("-" * 72)
        print(f"{'Ten mat hang':<20} {'Gia nhap':>14} {'Gia ban':>14} {'Ton kho':>10}")
        print("-" * 72)

        for mat_hang in self.kho_hang:
            gia_nhap = self.dinh_dang_tien(mat_hang["gia_nhap"])
            gia_ban = self.dinh_dang_tien(mat_hang["gia_ban"])
            print(
                f"{mat_hang['ten']:<20} {gia_nhap:>14} "
                f"{gia_ban:>14} {mat_hang['so_luong_ton']:>10}"
            )

        print("-" * 72)
        print(f"So ban thieu     : {len(self.so_ban_thieu)} don")
        print("=" * 72)

    def _tim_mat_hang(self, ten_mat_hang):
        for mat_hang in self.kho_hang:
            if mat_hang["ten"] == ten_mat_hang:
                return mat_hang
        return None

    def kiem_tra_su_kien_ngau_nhien(self):
        self.su_kien_hien_tai = None

        if random.random() >= 0.5:
            print("Hom nay la mot ngay binh thuong, khong co su kien dac biet.")
            return

        su_kien = random.choice(("mua_lon", "dam_cuoi", "tre_trom"))
        self.su_kien_hien_tai = su_kien

        if su_kien == "mua_lon":
            print("Su kien: Mua lon ngap duong! Hom nay khach se den it hon.")
            print("Ao mua ban duoc gap doi gia.")
        elif su_kien == "dam_cuoi":
            print("Su kien: Dam cuoi xom ben! Nhu cau nuoc da va bia tang vot.")
            self._xu_ly_dam_cuoi()
        else:
            keo_mut = self._tim_mat_hang("Kẹo mút")
            so_keo_mat = random.randint(1, 3)
            so_keo_mat = min(so_keo_mat, keo_mut["so_luong_ton"])
            keo_mut["so_luong_ton"] -= so_keo_mat
            print(
                f"Su kien: Tre con an trom! Cua hang mat {so_keo_mat} cai Keo mut."
            )

    def _xu_ly_dam_cuoi(self):
        doanh_thu = 0
        for ten_mat_hang in ("Nước đá", "Bia/Mồi nhậu"):
            mat_hang = self._tim_mat_hang(ten_mat_hang)
            so_luong_ban = min(random.randint(5, 10), mat_hang["so_luong_ton"])
            mat_hang["so_luong_ton"] -= so_luong_ban
            tien_ban = so_luong_ban * mat_hang["gia_ban"] * 2
            doanh_thu += tien_ban
            print(
                f"Da ban nhanh {so_luong_ban} {ten_mat_hang}, "
                f"thu ve {self.dinh_dang_tien(tien_ban)}."
            )

        self.so_tien += doanh_thu
        print(f"Doanh thu dac biet: {self.dinh_dang_tien(doanh_thu)}")

    def nhap_hang(self, input_func=input):
        print("\n===== DANH SACH HANG HOA NHAP =====")
        for so_thu_tu, mat_hang in enumerate(self.kho_hang, start=1):
            gia_nhap = self.dinh_dang_tien(mat_hang["gia_nhap"])
            print(f"{so_thu_tu}. {mat_hang['ten']:<20} - Gia nhap: {gia_nhap}")

        try:
            lua_chon = int(input_func("Ban muon nhap mat hang so may? ").strip())
            so_luong = int(input_func("Ban muon nhap bao nhieu? ").strip())
        except ValueError:
            print("Lua chon va so luong phai la so nguyen.")
            return

        if not 1 <= lua_chon <= len(self.kho_hang):
            print("Mat hang khong ton tai.")
            return

        if so_luong <= 0:
            print("So luong nhap phai lon hon 0.")
            return

        mat_hang = self.kho_hang[lua_chon - 1]
        tong_tien = mat_hang["gia_nhap"] * so_luong

        if self.so_tien < tong_tien:
            print("Bạn không đủ tiền, hãy bán thêm hàng")
            return

        self.so_tien -= tong_tien
        mat_hang["so_luong_ton"] += so_luong
        print(
            f"Nhập hàng thành công: {so_luong} {mat_hang['ten']}. "
            f"Da thanh toan {self.dinh_dang_tien(tong_tien)}."
        )

    def xem_so_ban_thieu_va_doi_no(self, input_func=input):
        if not self.so_ban_thieu:
            print("So ban thieu dang trong.")
            return

        print("\n===== SO BAN THIEU =====")
        for ten_khach, so_tien_no in self.so_ban_thieu.items():
            print(f"- {ten_khach}: {self.dinh_dang_tien(so_tien_no)}")

        ten_khach = input_func("Nhap ten nguoi ban muon di doi no: ").strip()
        if ten_khach not in self.so_ban_thieu:
            print("Khong tim thay nguoi nay trong so ban thieu.")
            return

        so_tien_no = self.so_ban_thieu[ten_khach]
        if random.random() < 0.7:
            self.so_tien += so_tien_no
            del self.so_ban_thieu[ten_khach]
            print(
                f"Doi no thanh cong tu {ten_khach}, thu ve "
                f"{self.dinh_dang_tien(so_tien_no)}."
            )
        else:
            print(f"{ten_khach} hen ngay mai moi tra no.")

    def mo_cua_ban_hang(self, input_func=input):
        if self.su_kien_hien_tai == "mua_lon":
            so_khach = random.randint(1, 2)
        else:
            so_khach = random.randint(2, 4)
        doanh_thu_trong_ngay = 0
        ten_khach_hang = ["Chú Bảy", "Bà Tư", "Anh Năm", "Cô Lan"]

        print(f"\nMo cua ban hang: hom nay co {so_khach} vi khach.")

        for so_thu_tu_khach in range(1, so_khach + 1):
            mat_hang = random.choice(self.kho_hang)
            so_luong_mua = random.randint(1, 3)
            print(
                f"Khach {so_thu_tu_khach} hoi mua {so_luong_mua} "
                f"{mat_hang['ten']}."
            )

            if mat_hang["so_luong_ton"] >= so_luong_mua:
                gia_ban = mat_hang["gia_ban"]
                if self.su_kien_hien_tai == "mua_lon" and mat_hang["ten"] == "Áo mưa":
                    gia_ban *= 2
                tien_ban = so_luong_mua * gia_ban
                if random.random() < 0.3:
                    ten_khach = random.choice(ten_khach_hang)
                    print(f"{ten_khach} xin mua thieu {self.dinh_dang_tien(tien_ban)}.")
                    dong_y = input_func("Ban co dong y cho no khong? (Y/N): ").strip().upper()

                    if dong_y == "Y":
                        mat_hang["so_luong_ton"] -= so_luong_mua
                        self.so_ban_thieu[ten_khach] = (
                            self.so_ban_thieu.get(ten_khach, 0) + tien_ban
                        )
                        print(
                            f"Da ghi so cho {ten_khach}: "
                            f"{self.dinh_dang_tien(tien_ban)}."
                        )
                    else:
                        print("Ban khong dong y cho no, khach roi di.")
                    continue

                mat_hang["so_luong_ton"] -= so_luong_mua
                doanh_thu_trong_ngay += tien_ban
                print(
                    f"Đã bán {so_luong_mua} món cho khách, "
                    f"thu về {self.dinh_dang_tien(tien_ban)}"
                )
            else:
                print("Hết hàng rồi, khách chửi thề rồi bỏ đi")

        self.so_tien += doanh_thu_trong_ngay
        print(
            f"Ket thuc ngay ban hang. Doanh thu: "
            f"{self.dinh_dang_tien(doanh_thu_trong_ngay)}"
        )
        print(f"So tien hien tai: {self.dinh_dang_tien(self.so_tien)}")
        self.ngay_hien_tai += 1
        print(f"Da het ngay. Chuyen sang Ngay {self.ngay_hien_tai}.")
        self.kiem_tra_su_kien_ngau_nhien()

    def chay_game(self):
        while True:
            print(f"\n===== MENU NGAY {self.ngay_hien_tai} =====")
            print("1. Mo cua ban hang")
            print("2. Doi xe ba gac de nhap hang")
            print("3. Xem so ban thieu & di doi no")
            print("4. Kiem tra kho hang")
            print("5. Dong cua di ngu")
            print("6. Thoat game")

            lua_chon = input("Nhap lua chon cua ban: ").strip()

            if lua_chon == "1":
                self.mo_cua_ban_hang()
            elif lua_chon == "2":
                self.nhap_hang()
            elif lua_chon == "3":
                self.xem_so_ban_thieu_va_doi_no()
            elif lua_chon == "4":
                self.hien_thi_thong_ke()
            elif lua_chon == "5":
                self.ngay_hien_tai += 1
                print(f"Cua hang da dong. Chao mung den Ngay {self.ngay_hien_tai}!")
                self.kiem_tra_su_kien_ngau_nhien()
            elif lua_chon == "6":
                print("Cam on ban da choi. Hen gap lai!")
                break
            else:
                print("Lua chon khong hop le. Vui long nhap tu 1 den 6.")


class GiaoDienGame:
    SAVE_FILE = "savegame.json"

    def __init__(self, root):
        self.root = root
        self.root.title("Cua hang tap hoa")
        self.root.geometry("1000x760")
        self.root.minsize(860, 650)
        self.game = None
        self.status_text = None
        self.canvas = None
        self.background_image = None
        self.background_size = None
        self.player_image = None
        self.activity_image = None
        self.activity_image_name = None
        self.yard_images = {}
        self.rest_background_image = None
        self.rest_background_size = None
        self.player_x = 120
        self.player_y = 155
        self.location = "shop"
        self.customers = []
        self.customer_waiting = False
        self.customer_timer = None
        self.shop_open = True
        self.activity = "counter"
        self.pending_delivery = None
        self.create_style()
        self.show_main_menu()

    def create_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 28, "bold"), foreground="#17324d")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 12), foreground="#527089")
        style.configure("Menu.TButton", font=("Segoe UI", 13, "bold"), padding=(18, 11))
        style.configure("Game.TButton", font=("Segoe UI", 11), padding=8)

    def clear_window(self):
        for key in ("<Up>", "<Down>", "<Left>", "<Right>"):
            self.root.unbind_all(key)
        for child in self.root.winfo_children():
            child.destroy()

    def show_main_menu(self):
        self.clear_window()
        wrapper = ttk.Frame(self.root, padding=48)
        wrapper.pack(expand=True, fill="both")
        ttk.Label(wrapper, text="CỬA HÀNG TẠP HÓA", style="Title.TLabel").pack(pady=(35, 5))
        ttk.Label(wrapper, text="Quản lý cửa hàng của bạn qua từng ngày", style="Subtitle.TLabel").pack(pady=(0, 28))
        buttons = ttk.Frame(wrapper)
        buttons.pack()
        ttk.Button(buttons, text="Vào game mới", style="Menu.TButton", command=self.new_game).pack(fill="x", pady=5)
        ttk.Button(buttons, text="Tiếp tục", style="Menu.TButton", command=self.continue_game).pack(fill="x", pady=5)
        ttk.Button(buttons, text="Lưu game", style="Menu.TButton", command=self.save_from_menu).pack(fill="x", pady=5)
        ttk.Button(buttons, text="Hướng dẫn", style="Menu.TButton", command=self.show_help).pack(fill="x", pady=5)
        ttk.Button(buttons, text="Thoát", style="Menu.TButton", command=self.root.destroy).pack(fill="x", pady=5)

    def new_game(self):
        self.game = CuaHangTapHoa()
        self.location = "shop"
        self.shop_open = True
        self.activity = "counter"
        self.prepare_customers()
        self.show_game()

    def continue_game(self):
        if not os.path.exists(self.SAVE_FILE):
            messagebox.showinfo("Tiếp tục", "Chưa có bản lưu. Hãy bắt đầu game mới.")
            return
        try:
            with open(self.SAVE_FILE, "r", encoding="utf-8") as save_file:
                data = json.load(save_file)
            self.game = CuaHangTapHoa()
            self.game.so_tien = data["so_tien"]
            self.game.ngay_hien_tai = data["ngay_hien_tai"]
            self.game.kho_hang = data["kho_hang"]
            self.game.so_ban_thieu = data["so_ban_thieu"]
            self.game.su_kien_hien_tai = data.get("su_kien_hien_tai")
            self.pending_delivery = data.get("pending_delivery")
            self.location = data.get("location", "shop")
            self.shop_open = data.get("shop_open", True)
            self.activity = data.get("activity", "counter")
            self.set_location_position()
            self.prepare_customers()
            self.show_game()
            self.write_status("Đã tải bản lưu thành công.")
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            messagebox.showerror("Lỗi tải game", "Bản lưu không hợp lệ hoặc đã bị hỏng.")

    def save_game(self):
        if self.game is None:
            messagebox.showinfo("Lưu game", "Bạn chưa vào game.")
            return
        data = {
            "so_tien": self.game.so_tien,
            "ngay_hien_tai": self.game.ngay_hien_tai,
            "kho_hang": self.game.kho_hang,
            "so_ban_thieu": self.game.so_ban_thieu,
            "su_kien_hien_tai": self.game.su_kien_hien_tai,
            "pending_delivery": self.pending_delivery,
            "location": self.location,
            "shop_open": self.shop_open,
            "activity": self.activity,
        }
        try:
            with open(self.SAVE_FILE, "w", encoding="utf-8") as save_file:
                json.dump(data, save_file, ensure_ascii=False, indent=2)
            self.write_status("Đã lưu game vào savegame.json.")
        except OSError as error:
            messagebox.showerror("Lỗi lưu game", f"Không thể lưu game: {error}")

    def save_from_menu(self):
        if self.game is None:
            messagebox.showinfo("Lưu game", "Hãy vào game trước khi lưu.")
        else:
            self.save_game()

    def show_help(self):
        messagebox.showinfo(
            "Hướng dẫn",
            "Khách sẽ đứng trước quầy và nói món đồ họ muốn mua. Bấm 'Bán cho khách' để giao dịch.\n\n"
            "Tiền khách đưa có thể vừa đủ, dư tiền cần thối hoặc bị thiếu.\n"
            "Đạp xe sang cửa hàng lớn để đặt hàng. Chuyến hàng sẽ được chở về khi sang ngày mới.\n\n"
            "Bấm 'Tạm đóng cửa' để nghỉ ở võng, ăn cơm hoặc đi lấy hàng.\n"
            "Khi quầy mở cửa, bấm trực tiếp vào khách đang đứng trước quầy để bán hàng.\n\n"
            "Hãy theo dõi tiền và tồn kho để cửa hàng luôn có lãi.",
        )

    def show_game(self):
        self.clear_window()
        outer = ttk.Frame(self.root, padding=20)
        outer.pack(expand=True, fill="both")
        header = ttk.Frame(outer)
        header.pack(fill="x")
        self.stats_label = ttk.Label(header, font=("Segoe UI", 14, "bold"))
        self.stats_label.pack(side="left")
        ttk.Button(header, text="Lưu game", command=self.save_game).pack(side="right", padx=4)
        ttk.Button(header, text="Menu chính", command=self.show_main_menu).pack(side="right", padx=4)
        ttk.Separator(outer).pack(fill="x", pady=14)
        scene_header = ttk.Frame(outer)
        scene_header.pack(fill="x")
        if self.location == "interior":
            location_title = "Bên trong Tạp hóa Bà 6"
        elif self.location == "shop":
            location_title = "Tạp hóa Bà 6"
        else:
            location_title = "Siêu thị Cô Ba"
        ttk.Label(scene_header, text=location_title, font=("Segoe UI", 12, "bold")).pack(side="left")
        ttk.Label(scene_header, text="Dùng các phím mũi tên để di chuyển Bà 6", foreground="#527089").pack(side="right")
        self.canvas = tk.Canvas(outer, height=350, bg="#b8e1ed", highlightthickness=1, highlightbackground="#7da5af")
        self.canvas.pack(fill="x", pady=(5, 12))
        self.canvas.configure(takefocus=1)
        self.canvas.tag_bind("customer", "<Button-1>", self.click_customer)
        for key in ("<Up>", "<Down>", "<Left>", "<Right>"):
            self.root.bind_all(key, self.move_player)
        self.root.after(100, self.focus_canvas)
        self.draw_scene()
        actions = ttk.Frame(outer)
        actions.pack(fill="x")
        commands = [
            ("Bán cho khách", self.serve_customer),
            ("Tạm đóng cửa", self.close_shop),
            ("Mở cửa lại", self.open_shop),
            ("Nghỉ ở võng", self.rest_at_hammock),
            ("Ăn cơm", self.eat_meal),
            ("Đạp xe đi / về", self.travel_to_supplier),
            ("Nhập hàng tại siêu thị", self.place_order),
            ("Nhận chuyến hàng", self.receive_delivery),
            ("Xem sổ nợ / Đòi nợ", self.collect_debt),
            ("Xem kho hàng", self.show_inventory),
            ("Đóng cửa sang ngày mới", self.close_day),
        ]
        for index, (label, command) in enumerate(commands):
            ttk.Button(actions, text=label, style="Game.TButton", command=command).grid(
                row=index // 3, column=index % 3, sticky="ew", padx=4, pady=4
            )
        for column in range(3):
            actions.columnconfigure(column, weight=1)
        self.status_text = tk.Text(outer, height=16, state="disabled", wrap="word", font=("Consolas", 10))
        self.status_text.pack(fill="both", expand=True, pady=(15, 0))
        outer.update_idletasks()
        self.refresh_stats()
        self.root.after_idle(self.redraw_scene_when_ready)
        self.root.after(150, self.redraw_scene_when_ready)

    def focus_canvas(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            self.canvas.focus_force()

    def redraw_scene_when_ready(self):
        if self.canvas is not None and self.canvas.winfo_exists():
            self.draw_scene()

    def prepare_customers(self):
        customer_names = ["Chú Bảy", "Bà Tư", "Anh Năm", "Cô Lan", "Bé Na"]
        self.customers = []
        self.customer_waiting = False
        if self.customer_timer is not None:
            self.root.after_cancel(self.customer_timer)
            self.customer_timer = None
        for name in random.sample(customer_names, random.randint(2, 4)):
            item = random.choice(self.game.kho_hang)
            self.customers.append({
                "ten": name,
                "mat_hang": item["ten"],
                "so_luong": random.randint(1, 3),
            })

    def click_customer(self, _event):
        self.serve_customer()
        return "break"

    def close_shop(self):
        if self.location != "shop":
            self.write_status("Bà 6 cần đạp xe về quầy trước khi đóng cửa.")
            return
        if not self.shop_open:
            self.write_status("Quầy đã tạm đóng cửa rồi.")
            return
        self.shop_open = False
        self.activity = "counter"
        self.customers = []
        self.customer_waiting = False
        if self.customer_timer is not None:
            self.root.after_cancel(self.customer_timer)
            self.customer_timer = None
        self.write_status("Đã tạm đóng cửa. Khách sẽ không vào cho đến khi Bà 6 mở cửa lại.")

    def open_shop(self):
        if self.location == "interior":
            self.location = "shop"
            self.shop_open = True
            self.activity = "counter"
            self.set_location_position()
            self.prepare_customers()
            self.write_status("Bà 6 đã ra quầy và mở cửa đón khách.")
            self.draw_scene()
            return
        if self.location != "shop":
            self.write_status("Bà 6 đang ở cửa hàng lớn, chưa thể mở quầy tại đây.")
            return
        self.shop_open = True
        self.activity = "counter"
        self.set_location_position()
        self.prepare_customers()
        self.write_status("Tạp hóa Bà 6 đã mở cửa. Khách bắt đầu lần lượt đến quầy.")

    def rest_at_hammock(self):
        if self.shop_open:
            self.write_status("Hãy tạm đóng cửa trước khi nghỉ ở võng.")
            return
        self.activity = "hammock"
        self.location = "interior"
        self.player_x = 380
        self.player_y = 126
        self.write_status("Bà 6 đang nằm nghỉ trên võng trong tiệm.\n\nNhấn 'Mở cửa lại' để ra quầy.")
        self.draw_scene()

    def eat_meal(self):
        if self.shop_open:
            self.write_status("Hãy tạm đóng cửa trước khi ngồi ăn cơm.")
            return
        self.activity = "table"
        self.location = "interior"
        self.player_x = 420
        self.player_y = 126
        self.write_status("Bà 6 đang ngồi ăn cơm ở bàn ăn.\n\nNhấn 'Mở cửa lại' để ra quầy.")
        self.draw_scene()

    def set_location_position(self):
        if self.location == "shop":
            self.player_x, self.player_y = 120, 155
        elif self.location == "supplier":
            self.player_x, self.player_y = 120, 155
        elif self.activity == "hammock":
            self.player_x, self.player_y = 380, 126
        else:
            self.player_x, self.player_y = 420, 126

    def debt_book_text(self):
        if not self.game.so_ban_thieu:
            return "SỔ NỢ\n\nHiện không có người nào thiếu nợ cửa hàng."
        debt_lines = ["SỔ NỢ", ""]
        for customer_name, debt in self.game.so_ban_thieu.items():
            debt_lines.append(f"- {customer_name}: {self.game.dinh_dang_tien(debt)}")
        return "\n".join(debt_lines)

    def wait_for_next_customer(self):
        self.customer_waiting = True
        self.draw_scene()
        self.customer_timer = self.root.after(2500, self.release_next_customer)

    def release_next_customer(self):
        self.customer_waiting = False
        self.customer_timer = None
        self.draw_scene()

    def serve_customer(self):
        if not self.shop_open:
            self.write_status("Quầy đang tạm đóng cửa, chưa thể bán hàng.")
            return
        if self.location != "shop":
            self.write_status("Bà 6 đang ở cửa hàng lớn. Hãy đạp xe về quầy trước.")
            return
        if self.customer_waiting:
            self.write_status("Khách tiếp theo đang trên đường đến. Vui lòng chờ một chút.")
            return
        if not self.customers:
            self.write_status("Hôm nay không còn khách nào trước quầy.")
            return

        customer = self.customers.pop(0)
        item = self.game._tim_mat_hang(customer["mat_hang"])
        quantity = customer["so_luong"]
        total = item["gia_ban"] * quantity
        output = [
            f"{customer['ten']} muốn mua {quantity} {item['ten']}.",
            f"Tổng tiền: {self.game.dinh_dang_tien(total)}.",
        ]
        if item["so_luong_ton"] < quantity:
            output.append("Quầy đã hết số lượng cần bán, khách đành bỏ đi.")
            self.wait_for_next_customer()
            self.write_status("\n".join(output))
            return

        payment_mode = random.choice(("exact", "change", "short"))
        if payment_mode == "short":
            paid = max(0, total - random.randint(1, max(1, total // 2)))
            output.append(f"Khách chỉ đưa {self.game.dinh_dang_tien(paid)}, đang thiếu tiền.")
            if not self.ask_yes_no("Khách xin ghi nợ phần còn thiếu. Bạn có đồng ý không?"):
                output.append("Bà 6 không đồng ý, khách cầm tiền ra về.")
                self.customers.append(customer)
                self.wait_for_next_customer()
                self.write_status("\n".join(output))
                return
            item["so_luong_ton"] -= quantity
            self.game.so_ban_thieu[customer["ten"]] = (
                self.game.so_ban_thieu.get(customer["ten"], 0) + total - paid
            )
            self.game.so_tien += paid
            output.append("Đã bán hàng và ghi phần còn thiếu vào sổ.")
        else:
            paid = total if payment_mode == "exact" else total + random.choice((1_000, 2_000, 5_000))
            item["so_luong_ton"] -= quantity
            self.game.so_tien += total
            if paid > total:
                output.append(
                    f"Khách đưa {self.game.dinh_dang_tien(paid)}. "
                    f"Bà 6 thối lại {self.game.dinh_dang_tien(paid - total)}."
                )
            else:
                output.append("Khách đưa vừa đủ tiền.")
        output.append(f"Còn {len(self.customers)} khách đang chờ trước quầy.")
        output.append("")
        output.append(self.debt_book_text())
        self.wait_for_next_customer()
        self.write_status("\n".join(output))

    def travel_to_supplier(self):
        if self.location == "interior":
            self.write_status("Hãy bấm 'Mở cửa lại' để ra quầy trước khi đạp xe đi lấy hàng.")
            return
        if self.location == "shop" and self.shop_open:
            self.write_status("Hãy bấm 'Tạm đóng cửa' trước khi đạp xe đi lấy hàng.")
            return
        self.location = "supplier" if self.location == "shop" else "shop"
        self.player_x = 120
        self.player_y = 155
        if self.location == "supplier":
            self.write_status("Bà 6 đạp xe đến cửa hàng lớn để nhập hàng.")
        else:
            self.shop_open = False
            self.activity = "counter"
            self.set_location_position()
            self.write_status("Bà 6 đã đạp xe về lại Tạp hóa Bà 6.")
        self.draw_scene()

    def place_order(self):
        if self.location != "supplier":
            self.write_status("Hãy đạp xe đến cửa hàng lớn trước khi đặt hàng.")
            return
        if self.pending_delivery is not None:
            self.write_status("Đang có một chuyến hàng trên đường về. Hãy chờ nhận hàng.")
            return
        catalog_lines = ["DANH SÁCH HÀNG CÓ THỂ NHẬP", ""]
        for index, item in enumerate(self.game.kho_hang, start=1):
            catalog_lines.append(
                f"{index}. {item['ten']} - giá nhập: "
                f"{self.game.dinh_dang_tien(item['gia_nhap'])} - đang có: {item['so_luong_ton']}"
            )
        self.write_status("\n".join(catalog_lines))
        item_number = self.ask_integer("Nhập số thứ tự mặt hàng muốn mua:")
        quantity = self.ask_integer("Nhập số lượng muốn mua:")
        try:
            item = self.game.kho_hang[int(item_number) - 1]
            quantity = int(quantity)
        except (ValueError, IndexError):
            self.write_status("Mặt hàng và số lượng phải là số hợp lệ.")
            return
        if quantity <= 0:
            self.write_status("Số lượng phải lớn hơn 0.")
            return
        total = item["gia_nhap"] * quantity
        if self.game.so_tien < total:
            self.write_status("Bà 6 không đủ tiền để đặt chuyến hàng này.")
            return
        self.game.so_tien -= total
        self.pending_delivery = {
            "ten": item["ten"],
            "so_luong": quantity,
            "tong_tien": total,
        }
        self.write_status(
            "\n".join(catalog_lines)
            + "\n\n"
            + f"Đã đặt {quantity} {item['ten']}. Cửa hàng lớn đang chở hàng về "
            "sau khi Bà 6 đóng cửa.\n"
            + f"Đã thanh toán: {self.game.dinh_dang_tien(total)}. "
            + f"Số dư còn lại: {self.game.dinh_dang_tien(self.game.so_tien)}."
        )

    def receive_delivery(self):
        if self.pending_delivery is None:
            self.write_status("Hiện không có chuyến hàng nào đang chờ.")
            return
        delivery = self.pending_delivery
        item = self.game._tim_mat_hang(delivery["ten"])
        item["so_luong_ton"] += delivery["so_luong"]
        self.pending_delivery = None
        self.write_status(
            f"Xe giao hàng của cửa hàng lớn vừa đến. Đã nhận {delivery['so_luong']} "
            f"{delivery['ten']} và nhập vào kho."
        )

    def refresh_stats(self):
        if self.game is not None and hasattr(self, "stats_label"):
            self.stats_label.config(
                text=f"Ngày {self.game.ngay_hien_tai}    |    Tiền: {self.game.dinh_dang_tien(self.game.so_tien)}"
            )
        self.draw_scene()

    def draw_scene(self):
        if self.canvas is None:
            return
        canvas_width = max(self.canvas.winfo_width(), 680)
        canvas_height = max(self.canvas.winfo_height(), 350)
        self.canvas.delete("all")
        self.draw_background(canvas_width, canvas_height)

        if self.location == "interior":
            self.draw_interior_scene(canvas_width, canvas_height)
            self.draw_player()
            self.scale_foreground()
            return
        if self.location == "supplier":
            self.draw_supplier_scene(canvas_width)
            self.draw_player()
            self.scale_foreground()
            return

        self.draw_shop_scene(canvas_width)
        self.scale_foreground()

    def scale_foreground(self):
        vertical_scale = 1.35
        for item in self.canvas.find_all():
            tags = self.canvas.gettags(item)
            if "background" not in tags and "rest-background" not in tags:
                self.canvas.scale(item, 0, 0, 1, vertical_scale)

    def draw_shop_scene(self, canvas_width):
        shop_left = 32
        shop_right = 245
        self.canvas.create_polygon(
            shop_left - 10, 86, shop_left + 20, 50, shop_right - 20, 50, shop_right + 10, 86,
            fill="#9b6847", outline="#5f3e2e", width=2,
        )
        self.canvas.create_rectangle(shop_left + 10, 78, shop_right - 10, 177, fill="#b7784e", outline="#5f3e2e", width=2)
        self.canvas.create_rectangle(shop_left + 25, 91, shop_right - 25, 143, fill="#8fc0b4", outline="#4e756c", width=2)
        self.canvas.create_rectangle(shop_left + 22, 53, shop_right - 22, 75, fill="#f0d28a", outline="#825538", width=2)
        self.canvas.create_text((shop_left + shop_right) // 2, 64, text="TẠP HÓA BÀ 6", fill="#5f3e2e", font=("Segoe UI", 10, "bold"))
        self.canvas.create_rectangle(shop_left + 10, 140, shop_right - 10, 157, fill="#70472f", outline="#4f3023", width=2)
        for product_x, product_color in ((shop_left + 35, "#f3bd4f"), (shop_left + 70, "#db6b56"), (shop_right - 55, "#e8e1bb")):
            self.canvas.create_rectangle(product_x, 121, product_x + 18, 140, fill=product_color, outline="#633822")
        self.canvas.create_text((shop_left + shop_right) // 2, 168, text="Mì tôm  •  Kẹo  •  Nước mắm", fill="#fff1cf", font=("Segoe UI", 8, "bold"))
        if not self.shop_open:
            self.canvas.create_rectangle(shop_left + 35, 103, shop_right - 35, 132, fill="#f7e5c3", outline="#8c2f2f", width=2)
            self.canvas.create_text((shop_left + shop_right) // 2, 118, text="TẠM ĐÓNG CỬA", fill="#8c2f2f", font=("Segoe UI", 9, "bold"))
        self.draw_home_yard(canvas_width)

        visible_customers = [] if self.customer_waiting else self.customers[:1]
        for customer in visible_customers:
            customer_x = 315
            self.canvas.create_oval(customer_x - 13, 126, customer_x + 13, 152, fill="#f0a989", outline="#8b5748", tags="customer")
            self.canvas.create_oval(customer_x - 16, 120, customer_x + 16, 127, fill="#59463c", outline="#3e302a", tags="customer")
            self.canvas.create_oval(customer_x - 14, 150, customer_x + 14, 192, fill="#d17963", outline="#8b5748", tags="customer")
            self.canvas.create_text(customer_x, 105, text=customer["ten"], fill="#49362d", font=("Segoe UI", 8, "bold"), tags="customer")
            self.draw_customer_bubble(customer, customer_x)
        self.canvas.create_text(70, 225, text="← ↑ ↓ →", fill="#315d50", font=("Segoe UI", 10, "bold"))
        self.draw_player()

    def draw_customer_bubble(self, customer, customer_x):
        bubble_left = customer_x - 100
        bubble_right = customer_x + 100
        self.canvas.create_oval(bubble_left, 22, bubble_right, 66, fill="white", outline="#6b5548", width=1, tags="customer")
        self.canvas.create_rectangle(bubble_left + 18, 32, bubble_right - 18, 56, fill="white", outline="", tags="customer")
        self.canvas.create_polygon(customer_x - 12, 63, customer_x, 78, customer_x + 18, 64, fill="white", outline="#6b5548", tags="customer")
        message = f"Bán cho {customer['so_luong']} {customer['mat_hang']}, Bà 6 ơi!"
        self.canvas.create_text(customer_x, 44, text=message, width=166, fill="#49362d", font=("Segoe UI", 8, "bold"), tags="customer")

    def draw_background(self, canvas_width, canvas_height):
        image_size = (canvas_width, canvas_height)
        if self.background_size != image_size:
            image_path = os.path.join(os.path.dirname(__file__), "img", "bg1.png")
            source = Image.open(image_path).convert("RGB")
            source_ratio = source.width / source.height
            canvas_ratio = canvas_width / canvas_height
            if source_ratio > canvas_ratio:
                resized_height = canvas_height
                resized_width = round(canvas_height * source_ratio)
            else:
                resized_width = canvas_width
                resized_height = round(canvas_width / source_ratio)
            source = source.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
            crop_left = max(0, (resized_width - canvas_width) // 2)
            crop_top = max(0, (resized_height - canvas_height) // 2)
            source = source.crop((crop_left, crop_top, crop_left + canvas_width, crop_top + canvas_height))
            self.background_image = ImageTk.PhotoImage(source)
            self.background_size = image_size
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw", tags="background")

    def draw_home_yard(self, canvas_width):
        patio_left = 245
        patio_right = canvas_width - 38
        self.canvas.create_text(42, 181, anchor="w", text="SÂN NHÀ BÀ 6", fill="#315d50", font=("Segoe UI", 9, "bold"))
        self.canvas.create_polygon(
            patio_left - 12, 198, patio_left + 18, 180, patio_right - 18, 180, patio_right + 12, 198,
            fill="#e8a35d", outline="#8b5a3c", width=2,
        )
        self.canvas.create_line(patio_left + 8, 196, patio_left + 8, 231, fill="#70472f", width=4)
        self.canvas.create_line(patio_right - 8, 196, patio_right - 8, 231, fill="#70472f", width=4)
        self.canvas.create_text((patio_left + patio_right) // 2, 190, text="MÁI CHE KHU BÀN ĂN", fill="white", font=("Segoe UI", 9, "bold"))
        self.draw_yard_image("6.png", patio_left + 105, 218)
        self.draw_yard_image("7.png", patio_left + 245, 218)

    def draw_yard_image(self, image_name, center_x, center_y):
        if image_name not in self.yard_images:
            image_path = os.path.join(os.path.dirname(__file__), "img", "character", image_name)
            source = Image.open(image_path).convert("RGBA")
            source.thumbnail((125, 84), Image.Resampling.LANCZOS)
            self.yard_images[image_name] = ImageTk.PhotoImage(source)
        self.canvas.create_image(
            center_x, center_y, image=self.yard_images[image_name], anchor="center", tags="yard-furniture"
        )

    def draw_property_fence(self, canvas_width):
        fence_left = 22
        fence_right = canvas_width - 22
        back_y = 94
        for segment_left, segment_right in ((fence_left, 215), (535, fence_right)):
            self.canvas.create_line(segment_left, back_y, segment_right, back_y, fill="#70472f", width=3)
            self.canvas.create_line(segment_left, back_y + 14, segment_right, back_y + 14, fill="#8b5a3c", width=2)
            for post_x in range(segment_left, segment_right + 1, 70):
                self.canvas.create_rectangle(post_x - 3, back_y - 6, post_x + 3, 216, fill="#70472f", outline="#583522")

    def draw_interior_scene(self, canvas_width, canvas_height):
        self.draw_rest_background(canvas_width, canvas_height)
        self.canvas.create_rectangle(0, 0, canvas_width, 42, fill="#b87954", outline="")
        self.canvas.create_text(40, 22, anchor="w", text="BÊN TRONG TẠP HÓA BÀ 6", fill="white", font=("Segoe UI", 14, "bold"))
        self.canvas.create_rectangle(35, 65, 210, 165, fill="#f7edd8", outline="#ad8059", width=2)
        self.canvas.create_text(122, 80, text="Tủ hàng", fill="#704a35", font=("Segoe UI", 10, "bold"))
        for index, color in enumerate(("#f3bd4f", "#db6b56", "#83a95d", "#e8e1bb")):
            left = 55 + index * 35
            self.canvas.create_rectangle(left, 112, left + 24, 143, fill=color, outline="#604b3c")
        self.canvas.create_rectangle(270, 58, 530, 165, fill="#f2e0bd", outline="#784f3b", width=2)
        self.canvas.create_text(290, 72, anchor="w", text="KHU NGHỈ", fill="#784f3b", font=("Segoe UI", 9, "bold"))
        if self.activity == "hammock":
            self.draw_activity_image("2.png")
            self.canvas.create_text(400, 150, text="Võng nghỉ", fill="#6b4938", font=("Segoe UI", 9, "bold"))
        else:
            self.draw_activity_image("3.png")
            self.canvas.create_text(400, 150, text="Bàn ăn", fill="#6b4938", font=("Segoe UI", 9, "bold"))

    def draw_rest_background(self, canvas_width, canvas_height):
        image_size = (canvas_width, canvas_height)
        if self.rest_background_size != image_size:
            image_path = os.path.join(os.path.dirname(__file__), "img", "character", "4.png")
            source = Image.open(image_path).convert("RGB")
            source_ratio = source.width / source.height
            canvas_ratio = canvas_width / canvas_height
            if source_ratio > canvas_ratio:
                resized_height = canvas_height
                resized_width = round(canvas_height * source_ratio)
            else:
                resized_width = canvas_width
                resized_height = round(canvas_width / source_ratio)
            source = source.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
            crop_left = max(0, (resized_width - canvas_width) // 2)
            crop_top = max(0, (resized_height - canvas_height) // 2)
            source = source.crop((crop_left, crop_top, crop_left + canvas_width, crop_top + canvas_height))
            self.rest_background_image = ImageTk.PhotoImage(source)
            self.rest_background_size = image_size
        self.canvas.create_image(0, 0, image=self.rest_background_image, anchor="nw", tags="rest-background")

    def draw_activity_image(self, image_name):
        image_path = os.path.join(os.path.dirname(__file__), "img", "character", image_name)
        source = Image.open(image_path).convert("RGBA")
        source.thumbnail((230, 125), Image.Resampling.LANCZOS)
        self.activity_image = ImageTk.PhotoImage(source)
        self.activity_image_name = image_name
        self.canvas.create_image(400, 112, image=self.activity_image, anchor="center", tags="activity")

    def draw_rest_area(self, shop_left, shop_right):
        room_left = shop_left + 22
        room_right = shop_right - 22
        self.canvas.create_rectangle(room_left, 68, room_right, 151, fill="#f2e0bd", outline="#784f3b", width=2)
        self.canvas.create_text(room_left + 45, 78, text="KHU NGHỈ", fill="#784f3b", font=("Segoe UI", 8, "bold"))
        if self.activity == "hammock":
            hammock_left = room_left + 35
            hammock_right = room_right - 35
            self.canvas.create_line(hammock_left, 82, hammock_left, 143, fill="#6b4938", width=4)
            self.canvas.create_line(hammock_right, 82, hammock_right, 143, fill="#6b4938", width=4)
            self.canvas.create_line(hammock_left, 88, hammock_right, 88, fill="#6b4938", width=3)
            self.canvas.create_line(
                hammock_left + 5, 95,
                hammock_left + 42, 112,
                (hammock_left + hammock_right) // 2, 119,
                hammock_right - 42, 112,
                hammock_right - 5, 95,
                fill="#d28365", width=6, smooth=True,
            )
            self.canvas.create_text((room_left + room_right) // 2, 143, text="Võng nghỉ của Bà 6", fill="#6b4938", font=("Segoe UI", 8, "bold"))
        elif self.activity == "table":
            table_left = room_left + 62
            table_right = room_right - 62
            self.canvas.create_rectangle(table_left, 116, table_right, 132, fill="#8b5033", outline="#633822", width=2)
            self.canvas.create_rectangle(table_left + 12, 132, table_left + 25, 149, fill="#633822", outline="")
            self.canvas.create_rectangle(table_right - 25, 132, table_right - 12, 149, fill="#633822", outline="")
            self.canvas.create_oval((table_left + table_right) // 2 - 10, 105, (table_left + table_right) // 2 + 10, 115, fill="#e17b4c", outline="#633822")
            self.canvas.create_text((room_left + room_right) // 2, 143, text="Bàn ăn của Bà 6", fill="#6b4938", font=("Segoe UI", 8, "bold"))

    def draw_supplier_scene(self, canvas_width):
        shop_left = canvas_width // 2 - 205
        shop_right = canvas_width // 2 + 205
        self.canvas.create_rectangle(shop_left, 45, shop_right, 180, fill="#d8d2c5", outline="#55524b", width=3)
        self.canvas.create_polygon(
            shop_left - 20, 47, shop_left + 30, 8, shop_right - 30, 8, shop_right + 20, 47,
            fill="#526b83", outline="#3a4b5b", width=3,
        )
        self.canvas.create_text((shop_left + shop_right) // 2, 29, text="SIÊU THỊ CÔ BA", fill="white", font=("Segoe UI", 14, "bold"))
        self.canvas.create_rectangle(shop_left + 30, 75, shop_right - 30, 145, fill="#9dc4c9", outline="#455d65", width=2)
        for index, color in enumerate(("#f3bd4f", "#db6b56", "#83a95d", "#e8e1bb", "#d1844e")):
            left = shop_left + 48 + index * 62
            self.canvas.create_rectangle(left, 115, left + 28, 145, fill=color, outline="#604b3c")
        self.canvas.create_rectangle(shop_left + 12, 145, shop_right - 12, 160, fill="#405a70", outline="#2d3e4d", width=2)
        self.canvas.create_text((shop_left + shop_right) // 2, 170, text="Cửa hàng lớn - nhận đặt hàng sỉ", fill="#49362d", font=("Segoe UI", 9, "bold"))
        self.canvas.create_oval(65, 179, 125, 239, outline="#3d5961", width=4)
        self.canvas.create_oval(126, 179, 186, 239, outline="#3d5961", width=4)
        self.canvas.create_line(95, 209, 156, 209, fill="#3d5961", width=3)
        self.canvas.create_line(126, 209, 111, 190, fill="#3d5961", width=3)
        self.canvas.create_text(240, 222, text="Xe đạp của Bà 6", fill="#315d50", font=("Segoe UI", 10, "bold"))

    def draw_player(self):
        if self.canvas is None:
            return
        x, y = self.player_x, self.player_y
        self.canvas.delete("player")
        if self.player_image is None:
            image_path = os.path.join(os.path.dirname(__file__), "img", "character", "1.png")
            source = Image.open(image_path).convert("RGBA")
            source.thumbnail((72, 108), Image.Resampling.LANCZOS)
            self.player_image = ImageTk.PhotoImage(source)
        self.canvas.create_image(x, y, image=self.player_image, anchor="center", tags="player")
        self.canvas.create_text(x, y + 66, text="Bà 6", fill="#315d50", font=("Segoe UI", 9, "bold"), tags="player")

    def move_player(self, event):
        movement = {"Up": (0, -12), "Down": (0, 12), "Left": (-12, 0), "Right": (12, 0)}
        if event.keysym not in movement:
            return
        dx, dy = movement[event.keysym]
        canvas_width = max(self.canvas.winfo_width(), 680)
        self.player_x = min(max(40, self.player_x + dx), canvas_width - 40)
        self.player_y = min(max(70, self.player_y + dy), 170)
        self.draw_scene()
        self.canvas.focus_set()

    def write_status(self, text):
        if self.status_text is None:
            return
        self.status_text.config(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.insert("end", text)
        self.status_text.config(state="disabled")
        self.refresh_stats()

    def run_action(self, action):
        output = StringIO()
        with redirect_stdout(output):
            action()
        self.write_status(output.getvalue() or "Đã hoàn tất thao tác.")

    def run_legacy_shop(self):
        self.run_action(lambda: self.game.mo_cua_ban_hang(input_func=self.ask_yes_no))

    def buy_stock(self):
        self.run_action(lambda: self.game.nhap_hang(input_func=self.ask_integer))

    def collect_debt(self):
        if not self.game.so_ban_thieu:
            self.write_status(self.debt_book_text())
            return

        debt_book = self.debt_book_text()
        self.write_status(debt_book + "\n\nĐang chờ bạn chọn người để đi đòi.")

        customer_name = self.ask_string("Nhập tên người muốn đi đòi nợ:").strip()
        if customer_name not in self.game.so_ban_thieu:
            self.write_status(debt_book + f"\n\nKhông tìm thấy người nợ tên '{customer_name}'.")
            return

        debt = self.game.so_ban_thieu[customer_name]
        if random.random() < 0.7:
            self.game.so_tien += debt
            del self.game.so_ban_thieu[customer_name]
            result = f"Đòi nợ thành công từ {customer_name}, thu về {self.game.dinh_dang_tien(debt)}."
        else:
            result = f"{customer_name} hẹn ngày mai mới trả nợ."
        self.write_status(debt_book + "\n\n" + result + "\n\n" + self.debt_book_text())

    def show_inventory(self):
        self.run_action(self.game.hien_thi_thong_ke)

    def close_day(self):
        def close():
            self.game.ngay_hien_tai += 1
            print(f"Cửa hàng đã đóng. Chào mừng đến Ngày {self.game.ngay_hien_tai}!")
            if self.pending_delivery is not None:
                delivery = self.pending_delivery
                item = self.game._tim_mat_hang(delivery["ten"])
                item["so_luong_ton"] += delivery["so_luong"]
                self.pending_delivery = None
                print(
                    f"Xe giao hàng đã chở đến {delivery['so_luong']} {delivery['ten']}. "
                    "Hàng đã nhập vào kho."
                )
            self.location = "shop"
            self.set_location_position()
            self.prepare_customers()
            self.game.kiem_tra_su_kien_ngau_nhien()

        self.run_action(close)

    def ask_integer(self, prompt):
        value = simpledialog.askinteger("Nhập thông tin", prompt, parent=self.root)
        return "" if value is None else str(value)

    def ask_string(self, prompt):
        value = simpledialog.askstring("Nhập thông tin", prompt, parent=self.root)
        return "" if value is None else value

    def ask_yes_no(self, prompt):
        return "Y" if messagebox.askyesno("Xác nhận", prompt, parent=self.root) else "N"


if __name__ == "__main__":
    root = tk.Tk()
    GiaoDienGame(root)
    root.mainloop()
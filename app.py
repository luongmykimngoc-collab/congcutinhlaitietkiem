import streamlit as st
st.image("logo.jpg.png")
# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰APP TÍNH TIỀN GỬI TIẾT KIỆM_LƯƠNG MỸ KIM NGỌC")
st.caption("Tính lãi đơn và lãi kép theo số tiền, kỳ hạn, lãi suất và hình thức nhận lãi.")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# =========================
# NHẬP DỮ LIỆU
# =========================
st.subheader("📌 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:
    tien_gui = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=1200,
        value=12,
        step=1
    )

with col2:
    loai_lai = st.selectbox(
        "Hình thức tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc_nhan_lai = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Lãnh lãi theo tháng",
            "Lãnh lãi theo quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

st.divider()

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính lãi", type="primary", use_container_width=True):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không hợp lệ.")
        st.stop()

    # Lãi suất theo tháng
    lai_suat_nam = lai_suat / 100
    lai_suat_thang = lai_suat_nam / 12

    # Số tháng của kỳ hạn
    so_thang = ky_han

    # =========================
    # LÃI ĐƠN
    # =========================
    if loai_lai == "Lãi đơn":

        tong_tien_lai = tien_gui * lai_suat_thang * so_thang

        # Lãi định kỳ
        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
            lai_dinh_ky = tien_gui * lai_suat_thang

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
            lai_dinh_ky = tien_gui * lai_suat_thang * 3

        else:
            lai_dinh_ky = tong_tien_lai

        tong_goc_lai = tien_gui + tong_tien_lai

    # =========================
    # LÃI KÉP
    # =========================
    else:

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":
            # Ghép lãi hàng tháng
            lai_dinh_ky = None

            tien_cuoi_ky = tien_gui * (
                (1 + lai_suat_thang) ** so_thang
            )

            tong_tien_lai = tien_cuoi_ky - tien_gui
            tong_goc_lai = tien_cuoi_ky

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":
            # Ghép lãi hàng quý
            lai_suat_quy = lai_suat_nam / 4
            so_quy = so_thang / 3

            # Xử lý cả trường hợp kỳ hạn không chia hết cho 3
            so_quy_day_du = int(so_thang // 3)
            so_thang_le = so_thang % 3

            tien_sau_quy = tien_gui * (
                (1 + lai_suat_quy) ** so_quy_day_du
            )

            if so_thang_le > 0:
                tien_sau_quy *= (
                    1 + lai_suat_thang * so_thang_le
                )

            tien_cuoi_ky = tien_sau_quy

            tong_tien_lai = tien_cuoi_ky - tien_gui
            tong_goc_lai = tien_cuoi_ky

            # Lãi của một quý đầy đủ tại thời điểm đầu kỳ
            lai_dinh_ky = tien_gui * lai_suat_quy

        else:
            # Lãnh lãi cuối kỳ:
            # giả định lãi được nhập gốc theo tháng
            tien_cuoi_ky = tien_gui * (
                (1 + lai_suat_thang) ** so_thang
            )

            tong_tien_lai = tien_cuoi_ky - tien_gui
            tong_goc_lai = tien_cuoi_ky

            lai_dinh_ky = tong_tien_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💵 Tiền lãi định kỳ",
            "Không áp dụng" if lai_dinh_ky is None
            else format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "📈 Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    with col3:
        st.metric(
            "💰 Tổng gốc + lãi",
            format_money(tong_goc_lai)
        )

    # =========================
    # THÔNG TIN CHI TIẾT
    # =========================
    st.divider()

    st.subheader("📋 Chi tiết khoản gửi")

    details = {
        "Số tiền gửi": format_money(tien_gui),
        "Kỳ hạn": f"{ky_han} tháng",
        "Hình thức tính lãi": loai_lai,
        "Hình thức nhận lãi": hinh_thuc_nhan_lai,
        "Lãi suất": f"{lai_suat:.2f}%/năm",
        "Tổng tiền lãi": format_money(tong_tien_lai),
        "Tổng số tiền gốc và lãi": format_money(tong_goc_lai)
    }

    for key, value in details.items():
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.write(f"**{key}**")
        with col_b:
            st.write(value)

    # =========================
    # GHI CHÚ
    # =========================
    st.info(
        "Lưu ý: Đây là công cụ mô phỏng theo công thức lãi suất danh nghĩa "
        "nhập vào. Lãi suất thực tế của ngân hàng có thể áp dụng cách tính "
        "ngày gửi, ngày đáo hạn, số ngày trong năm và quy định riêng về "
        "nhập lãi vào gốc."
    )

# =========================================================
# PHẦN 2: VISUALIZING FINANCIAL GOALS
# =========================================================

st.divider()

st.header("🎯 2. Visualizing Financial Goals")
st.caption(
    "Biến mục tiêu tài chính thành một kế hoạch tiết kiệm cụ thể."
)

st.write(
    "Thay vì chỉ nhìn vào một con số lớn, hãy chọn mục tiêu "
    "và để ứng dụng tính ngược số tiền bạn cần tiết kiệm "
    "mỗi ngày, mỗi tuần hoặc mỗi tháng."
)

# =========================
# DANH SÁCH MỤC TIÊU
# =========================

muc_tieu = {

    "🚗 Mua xe":
        80_000_000,

    "📱 Đổi iPhone":
        30_000_000,

    "✈️ Đi du lịch":
        20_000_000,

    "💍 Đám cưới":
        200_000_000,

    "🏠 Mua nhà":
        2_000_000_000,

    "💻 Mua laptop":
        30_000_000,

    "🎓 Học tập":
        50_000_000,

    "💰 Mục tiêu khác":
        100_000_000
}

# =========================
# CHỌN MỤC TIÊU
# =========================

muc_tieu_chon = st.selectbox(
    "🎯 Bạn đang muốn tiết kiệm cho mục tiêu nào?",
    list(muc_tieu.keys())
)

# =========================
# SỐ TIỀN MỤC TIÊU
# =========================

if muc_tieu_chon == "💰 Mục tiêu khác":

    so_tien_muc_tieu = st.number_input(
        "💵 Số tiền mục tiêu (VNĐ)",
        min_value=1_000_000.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

else:

    so_tien_muc_tieu = st.number_input(
        "💵 Số tiền mục tiêu (VNĐ)",
        min_value=1_000_000.0,
        value=float(muc_tieu[muc_tieu_chon]),
        step=1_000_000.0,
        format="%.0f"
    )

# =========================
# THỜI GIAN
# =========================

col1, col2 = st.columns(2)

with col1:

    so_nam = st.number_input(
        "⏳ Thời gian thực hiện mục tiêu (năm)",
        min_value=0.1,
        max_value=100.0,
        value=3.0,
        step=0.5
    )

with col2:

    lai_suat_muc_tieu = st.number_input(
        "📈 Lãi suất dự kiến (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.2f"
    )

# =========================
# VỐN BAN ĐẦU
# =========================

von_ban_dau = st.number_input(
    "💰 Số tiền bạn đã có sẵn (VNĐ)",
    min_value=0.0,
    value=0.0,
    step=1_000_000.0,
    format="%.0f"
)

# =========================
# TẦN SUẤT TIẾT KIỆM
# =========================

tan_suat = st.selectbox(
    "📅 Bạn muốn tiết kiệm bao nhiêu lần?",
    [
        "Mỗi ngày",
        "Mỗi tuần",
        "Mỗi tháng"
    ]
)

# =========================================================
# TÍNH SỐ TIỀN CẦN TIẾT KIỆM
# =========================================================

if st.button(
    "🎯 Tính kế hoạch mục tiêu",
    type="primary",
    use_container_width=True
):

    if so_tien_muc_tieu <= von_ban_dau:

        st.success(
            "🎉 Bạn đã có đủ số tiền để thực hiện mục tiêu!"
        )

        st.metric(
            "Số tiền hiện có",
            format_money(von_ban_dau)
        )

    else:

        lai_suat_nam_decimal = (
            lai_suat_muc_tieu / 100
        )

        # =========================
        # XÁC ĐỊNH SỐ KỲ
        # =========================

        if tan_suat == "Mỗi ngày":

            so_ky = int(round(so_nam * 365))

            lai_suat_ky = (
                lai_suat_nam_decimal / 365
            )

        elif tan_suat == "Mỗi tuần":

            so_ky = int(round(so_nam * 52))

            lai_suat_ky = (
                lai_suat_nam_decimal / 52
            )

        else:

            so_ky = int(round(so_nam * 12))

            lai_suat_ky = (
                lai_suat_nam_decimal / 12
            )

        # =========================
        # GIÁ TRỊ VỐN BAN ĐẦU
        # SAU KHI TÍCH LŨY
        # =========================

        gia_tri_von_ban_dau = (
            von_ban_dau
            * ((1 + lai_suat_ky) ** so_ky)
        )

        so_tien_con_thieu = (
            so_tien_muc_tieu
            - gia_tri_von_ban_dau
        )

        # =========================
        # TÍNH TIỀN TIẾT KIỆM ĐỊNH KỲ
        # =========================

        if so_tien_con_thieu <= 0:

            tien_moi_ky = 0

        elif lai_suat_ky == 0:

            tien_moi_ky = (
                so_tien_con_thieu / so_ky
            )

        else:

            tien_moi_ky = (
                so_tien_con_thieu
                * lai_suat_ky
                / (
                    (1 + lai_suat_ky) ** so_ky
                    - 1
                )
            )

        # =========================
        # TỔNG TIỀN TỰ TIẾT KIỆM
        # =========================

        tong_tien_tu_tiet_kiem = (
            tien_moi_ky * so_ky
        )

        # =========================
        # TIỀN LÃI DỰ KIẾN
        # =========================

        tong_tien_dat_duoc = (
            gia_tri_von_ban_dau
            + tien_moi_ky
            * (
                ((1 + lai_suat_ky) ** so_ky - 1)
                / lai_suat_ky
            )
            if lai_suat_ky != 0
            else
            gia_tri_von_ban_dau
            + tong_tien_tu_tiet_kiem
        )

        tong_von_bo_vao = (
            von_ban_dau
            + tong_tien_tu_tiet_kiem
        )

        tien_lai_du_kien = (
            tong_tien_dat_duoc
            - tong_von_bo_vao
        )

        # =========================
        # QUY ĐỔI THEO NGÀY/TUẦN/THÁNG
        # =========================

        tien_moi_ngay = (
            tien_moi_ky
            if tan_suat == "Mỗi ngày"
            else tien_moi_ky / 7
            if tan_suat == "Mỗi tuần"
            else tien_moi_ky / 30
        )

        tien_moi_tuan = (
            tien_moi_ky
            if tan_suat == "Mỗi tuần"
            else tien_moi_ky * 7
            if tan_suat == "Mỗi ngày"
            else tien_moi_ky / 4.345
        )

        tien_moi_thang = (
            tien_moi_ky
            if tan_suat == "Mỗi tháng"
            else tien_moi_ky * 30
            if tan_suat == "Mỗi ngày"
            else tien_moi_ky * 4.345
        )

        # =========================
        # HIỂN THỊ MỤC TIÊU
        # =========================

        st.success(
            f"🎯 Mục tiêu: **{muc_tieu_chon}**"
        )

        st.metric(
            "💎 Số tiền mục tiêu",
            format_money(so_tien_muc_tieu)
        )

        # =========================
        # KẾT QUẢ CHÍNH
        # =========================

        st.subheader("💡 Kế hoạch tiết kiệm của bạn")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📅 Mỗi ngày",
                format_money(tien_moi_ngay)
            )

        with col2:

            st.metric(
                "📆 Mỗi tuần",
                format_money(tien_moi_tuan)
            )

        with col3:

            st.metric(
                "🗓️ Mỗi tháng",
                format_money(tien_moi_thang)
            )

        # =========================
        # PHÂN TÍCH TÀI CHÍNH
        # =========================

        st.divider()

        st.subheader("📊 Phân tích mục tiêu")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "💰 Vốn bạn tự bỏ vào",
                format_money(tong_von_bo_vao)
            )

        with col2:

            st.metric(
                "📈 Lãi dự kiến",
                format_money(tien_lai_du_kien)
            )

        with col3:

            st.metric(
                "🎯 Giá trị cuối kỳ",
                format_money(tong_tien_dat_duoc)
            )

        # =========================
        # TIẾN ĐỘ MỤC TIÊU
        # =========================

        st.divider()

        st.subheader("🚀 Tiến độ thực hiện mục tiêu")

        if so_tien_muc_tieu > 0:

            phan_tram_tien_goc = min(
                tong_von_bo_vao
                / so_tien_muc_tieu
                * 100,
                100
            )

            phan_tram_lai = min(
                tien_lai_du_kien
                / so_tien_muc_tieu
                * 100,
                100
            )

            st.progress(
                int(phan_tram_tien_goc)
            )

            st.write(
                f"Bạn đang xây dựng mục tiêu với "
                f"**{phan_tram_tien_goc:.1f}%** giá trị mục tiêu "
                f"từ số tiền tự tiết kiệm."
            )

        # =========================
        # THÔNG ĐIỆP ĐỘNG LỰC
        # =========================

        st.divider()

        if tien_lai_du_kien > 0:

            st.info(
                f"💡 Với kế hoạch này, bạn dự kiến tự tích lũy "
                f"{format_money(tong_von_bo_vao)} và có thêm "
                f"{format_money(tien_lai_du_kien)} tiền lãi. "
                f"Nhờ đó có thể đạt khoảng "
                f"{format_money(tong_tien_dat_duoc)} sau "
                f"{so_nam:g} năm."
            )

        else:

            st.info(
                "💡 Hãy duy trì khoản tiết kiệm định kỳ đều đặn "
                "để tiến gần hơn đến mục tiêu tài chính của bạn."
            )

        # =========================
        # GHI CHÚ
        # =========================

        st.caption(
            "⚠️ Đây là mô hình mô phỏng. Kết quả thực tế có thể "
            "khác do lãi suất ngân hàng, thời điểm gửi tiền, "
            "cách nhập lãi và số ngày thực tế trong năm."
        )
```

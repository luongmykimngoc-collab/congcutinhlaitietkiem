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
import streamlit as st
import math

# ============================================================
# CẤU HÌNH TRANG
# ============================================================

st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# ============================================================
# LOGO
# ============================================================

try:
    st.image("logo.jpg.png", width=180)
except:
    pass

st.title("💰 APP TÍNH TIỀN GỬI TIẾT KIỆM - LƯƠNG MỸ KIM NGỌC")

st.caption(
    "Tính lãi đơn, lãi kép và lập kế hoạch tiết kiệm để đạt mục tiêu tài chính."
)

# ============================================================
# HÀM ĐỊNH DẠNG TIỀN
# ============================================================

def format_money(value):
    return f"{value:,.0f} VNĐ".replace(",", ".")


# ============================================================
# PHẦN 1 - TÍNH TIỀN GỬI TIẾT KIỆM
# ============================================================

st.header("🏦 1. Tính tiền gửi tiết kiệm")

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

# ============================================================
# TÍNH TOÁN TIỀN GỬI
# ============================================================

if st.button(
    "🧮 Tính lãi",
    type="primary",
    use_container_width=True
):

    if tien_gui <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không hợp lệ.")
        st.stop()

    # Lãi suất năm dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Lãi suất tháng
    lai_suat_thang = lai_suat_nam / 12

    so_thang = ky_han

    # Biến kết quả
    lai_dinh_ky = None

    # ========================================================
    # LÃI ĐƠN
    # ========================================================

    if loai_lai == "Lãi đơn":

        tong_tien_lai = (
            tien_gui
            * lai_suat_thang
            * so_thang
        )

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

            lai_dinh_ky = (
                tien_gui
                * lai_suat_thang
            )

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

            lai_dinh_ky = (
                tien_gui
                * lai_suat_thang
                * 3
            )

        else:

            lai_dinh_ky = tong_tien_lai

        tong_goc_lai = (
            tien_gui
            + tong_tien_lai
        )

    # ========================================================
    # LÃI KÉP
    # ========================================================

    else:

        # ----------------------------------------------------
        # LÃNH LÃI THEO THÁNG
        # ----------------------------------------------------

        if hinh_thuc_nhan_lai == "Lãnh lãi theo tháng":

            tien_cuoi_ky = (
                tien_gui
                * ((1 + lai_suat_thang) ** so_thang)
            )

            tong_tien_lai = (
                tien_cuoi_ky
                - tien_gui
            )

            tong_goc_lai = tien_cuoi_ky

            lai_dinh_ky = None

        # ----------------------------------------------------
        # LÃNH LÃI THEO QUÝ
        # ----------------------------------------------------

        elif hinh_thuc_nhan_lai == "Lãnh lãi theo quý":

            lai_suat_quy = lai_suat_nam / 4

            so_quy_day_du = so_thang // 3
            so_thang_le = so_thang % 3

            tien_sau_quy = (
                tien_gui
                * ((1 + lai_suat_quy) ** so_quy_day_du)
            )

            if so_thang_le > 0:

                tien_sau_quy *= (
                    1
                    + lai_suat_thang * so_thang_le
                )

            tien_cuoi_ky = tien_sau_quy

            tong_tien_lai = (
                tien_cuoi_ky
                - tien_gui
            )

            tong_goc_lai = tien_cuoi_ky

            lai_dinh_ky = (
                tien_gui
                * lai_suat_quy
            )

        # ----------------------------------------------------
        # LÃNH LÃI CUỐI KỲ
        # ----------------------------------------------------

        else:

            tien_cuoi_ky = (
                tien_gui
                * ((1 + lai_suat_thang) ** so_thang)
            )

            tong_tien_lai = (
                tien_cuoi_ky
                - tien_gui
            )

            tong_goc_lai = tien_cuoi_ky

            lai_dinh_ky = tong_tien_lai

    # ========================================================
    # HIỂN THỊ KẾT QUẢ
    # ========================================================

    st.subheader("📊 Kết quả")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "💵 Tiền lãi định kỳ",
            "Không áp dụng"
            if lai_dinh_ky is None
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

    # ========================================================
    # CHI TIẾT
    # ========================================================

    st.divider()

    st.subheader("📋 Chi tiết khoản gửi")

    details = {

        "Số tiền gửi":
            format_money(tien_gui),

        "Kỳ hạn":
            f"{ky_han} tháng",

        "Hình thức tính lãi":
            loai_lai,

        "Hình thức nhận lãi":
            hinh_thuc_nhan_lai,

        "Lãi suất":
            f"{lai_suat:.2f}%/năm",

        "Tổng tiền lãi":
            format_money(tong_tien_lai),

        "Tổng số tiền gốc và lãi":
            format_money(tong_goc_lai)
    }

    for key, value in details.items():

        col_a, col_b = st.columns([1, 2])

        with col_a:
            st.write(f"**{key}**")

        with col_b:
            st.write(value)

    st.info(
        "Lưu ý: Đây là công cụ mô phỏng theo công thức lãi suất "
        "danh nghĩa nhập vào. Lãi suất thực tế của ngân hàng có thể "
        "áp dụng cách tính ngày gửi, ngày đáo hạn, số ngày trong năm "
        "và quy định riêng về nhập lãi vào gốc."
    )


# ============================================================
# PHẦN 2 - VISUALIZING FINANCIAL GOALS
# ============================================================

st.divider()

st.header("🎯 2. Visualizing Financial Goals")
st.subheader("✨ Biến mục tiêu thành kế hoạch tiết kiệm")

st.write(
    "Chọn một mục tiêu tài chính, nhập số tiền cần có, "
    "thời gian và lãi suất dự kiến. App sẽ tính ngược "
    "số tiền bạn cần tiết kiệm mỗi ngày, mỗi tuần và mỗi tháng."
)

# ============================================================
# CHỌN MỤC TIÊU
# ============================================================

muc_tieu = st.selectbox(
    "🎯 Bạn đang tiết kiệm cho mục tiêu nào?",
    [
        "🚗 Mua xe",
        "📱 Đổi iPhone",
        "✈️ Đi du lịch",
        "💍 Đám cưới",
        "🏠 Mua nhà",
        "🎓 Học tập",
        "💻 Mua laptop",
        "💰 Mục tiêu khác"
    ]
)

# ============================================================
# GỢI Ý SỐ TIỀN THEO MỤC TIÊU
# ============================================================

goi_y = {

    "🚗 Mua xe": 50_000_000,

    "📱 Đổi iPhone": 30_000_000,

    "✈️ Đi du lịch": 20_000_000,

    "💍 Đám cưới": 200_000_000,

    "🏠 Mua nhà": 2_000_000_000,

    "🎓 Học tập": 50_000_000,

    "💻 Mua laptop": 30_000_000,

    "💰 Mục tiêu khác": 100_000_000
}

# ============================================================
# THÔNG TIN MỤC TIÊU
# ============================================================

col1, col2 = st.columns(2)

with col1:

    muc_tieu_tien = st.number_input(
        "💵 Số tiền mục tiêu (VNĐ)",
        min_value=1_000_000.0,
        value=float(goi_y[muc_tieu]),
        step=1_000_000.0,
        format="%.0f"
    )

with col2:

    thoi_gian_nam = st.number_input(
        "⏳ Thời gian đạt mục tiêu (năm)",
        min_value=0.1,
        max_value=100.0,
        value=3.0,
        step=0.5
    )

lai_suat_muc_tieu = st.number_input(
    "📈 Lãi suất tiết kiệm dự kiến (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
    format="%.2f"
)

# ============================================================
# SỐ TIỀN ĐÃ CÓ
# ============================================================

tien_da_co = st.number_input(
    "💰 Số tiền bạn đã có sẵn (VNĐ)",
    min_value=0.0,
    value=0.0,
    step=1_000_000.0,
    format="%.0f"
)

# ============================================================
# NÚT TÍNH MỤC TIÊU
# ============================================================

if st.button(
    "🎯 Tính kế hoạch đạt mục tiêu",
    type="primary",
    use_container_width=True
):

    if muc_tieu_tien <= 0:

        st.error(
            "Số tiền mục tiêu phải lớn hơn 0."
        )

        st.stop()

    if thoi_gian_nam <= 0:

        st.error(
            "Thời gian phải lớn hơn 0."
        )

        st.stop()

    if tien_da_co >= muc_tieu_tien:

        st.success(
            "🎉 Chúc mừng! Bạn đã có đủ tiền để thực hiện mục tiêu."
        )

        st.metric(
            "Số tiền mục tiêu",
            format_money(muc_tieu_tien)
        )

        st.stop()

    # ========================================================
    # TÍNH TOÁN
    # ========================================================

    tien_can_tich_luy = (
        muc_tieu_tien
        - tien_da_co
    )

    # Số tháng
    so_thang = thoi_gian_nam * 12

    # Số tuần
    so_tuan = thoi_gian_nam * 52

    # Số ngày
    so_ngay = thoi_gian_nam * 365

    # --------------------------------------------------------
    # TRƯỜNG HỢP CÓ LÃI SUẤT
    # --------------------------------------------------------

    if lai_suat_muc_tieu > 0:

        lai_nam = (
            lai_suat_muc_tieu / 100
        )

        lai_thang = lai_nam / 12

        # ----------------------------------------------------
        # Khoản tiết kiệm đều hàng tháng
        #
        # FV = PMT × [((1+r)^n - 1) / r]
        #
        # PMT = FV × r / ((1+r)^n - 1)
        # ----------------------------------------------------

        tien_thang = (
            tien_can_tich_luy
            * lai_thang
            / (
                (1 + lai_thang) ** so_thang
                - 1
            )
        )

        # ----------------------------------------------------
        # Khoản tiết kiệm đều hàng tuần
        # ----------------------------------------------------

        lai_tuan = lai_nam / 52

        tien_tuan = (
            tien_can_tich_luy
            * lai_tuan
            / (
                (1 + lai_tuan) ** so_tuan
                - 1
            )
        )

        # ----------------------------------------------------
        # Khoản tiết kiệm đều hàng ngày
        # ----------------------------------------------------

        lai_ngay = lai_nam / 365

        tien_ngay = (
            tien_can_tich_luy
            * lai_ngay
            / (
                (1 + lai_ngay) ** so_ngay
                - 1
            )
        )

    # ========================================================
    # TRƯỜNG HỢP LÃI SUẤT = 0
    # ========================================================

    else:

        tien_thang = (
            tien_can_tich_luy
            / so_thang
        )

        tien_tuan = (
            tien_can_tich_luy
            / so_tuan
        )

        tien_ngay = (
            tien_can_tich_luy
            / so_ngay
        )

    # ========================================================
    # HIỂN THỊ KẾT QUẢ
    # ========================================================

    st.success(
        f"🎯 Mục tiêu của bạn: {muc_tieu}"
    )

    st.subheader("💡 Bạn cần tiết kiệm")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📅 Mỗi ngày",
            format_money(tien_ngay)
        )

    with col2:

        st.metric(
            "📆 Mỗi tuần",
            format_money(tien_tuan)
        )

    with col3:

        st.metric(
            "🗓️ Mỗi tháng",
            format_money(tien_thang)
        )

    # ========================================================
    # THÔNG TIN CHI TIẾT
    # ========================================================

    st.divider()

    st.subheader("📊 Chi tiết kế hoạch")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**🎯 Mục tiêu:** {muc_tieu}"
        )

        st.write(
            f"**💰 Số tiền cần có:** "
            f"{format_money(muc_tieu_tien)}"
        )

        st.write(
            f"**💵 Số tiền đã có:** "
            f"{format_money(tien_da_co)}"
        )

        st.write(
            f"**💸 Số tiền còn thiếu:** "
            f"{format_money(tien_can_tich_luy)}"
        )

    with col2:

        st.write(
            f"**⏳ Thời gian:** "
            f"{thoi_gian_nam:.1f} năm"
        )

        st.write(
            f"**📈 Lãi suất dự kiến:** "
            f"{lai_suat_muc_tieu:.2f}%/năm"
        )

        st.write(
            f"**📅 Số tháng:** "
            f"{so_thang:.0f} tháng"
        )

        st.write(
            f"**📆 Số tuần:** "
            f"{so_tuan:.0f} tuần"
        )

    # ========================================================
    # TRỰC QUAN HÓA MỤC TIÊU
    # ========================================================

    st.divider()

    st.subheader("📈 Hành trình đến mục tiêu")

    # Tính giá trị tích lũy theo từng tháng
    so_thang_int = max(1, math.ceil(so_thang))

    du_lieu = []

    for thang in range(
        0,
        so_thang_int + 1
    ):

        if lai_suat_muc_tieu > 0:

            gia_tri = (
                tien_da_co
                * ((1 + lai_thang) ** thang)
            )

            if thang > 0:

                gia_tri += (
                    tien_thang
                    * (
                        ((1 + lai_thang) ** thang - 1)
                        / lai_thang
                    )
                )

        else:

            gia_tri = (
                tien_da_co
                + tien_thang * thang
            )

        gia_tri = min(
            gia_tri,
            muc_tieu_tien
        )

        du_lieu.append(gia_tri)

    st.line_chart(
        du_lieu,
        height=350
    )

    # ========================================================
    # THANH TIẾN ĐỘ
    # ========================================================

    tien_hien_tai = tien_da_co

    if muc_tieu_tien > 0:

        progress = min(
            tien_hien_tai / muc_tieu_tien,
            1.0
        )

    else:

        progress = 0

    st.write(
        f"**Tiến độ hiện tại: "
        f"{progress * 100:.1f}%**"
    )

    st.progress(progress)

    # ========================================================
    # THÔNG ĐIỆP ĐỘNG LỰC
    # ========================================================

    if tien_thang < 1_000_000:

        st.success(
            "🌱 Mục tiêu này khá nhẹ nhàng! "
            "Chỉ cần duy trì đều đặn mỗi tháng là bạn "
            "có thể tiến gần đến mục tiêu."
        )

    elif tien_thang < 5_000_000:

        st.info(
            "💪 Hãy biến khoản tiết kiệm hàng tháng "
            "thành một khoản chi cố định trong ngân sách."
        )

    else:

        st.warning(
            "🔥 Mục tiêu khá lớn! Bạn có thể cân nhắc "
            "kéo dài thời gian hoặc tăng số tiền tiết kiệm "
            "ban đầu để giảm áp lực mỗi tháng."
        )

# ============================================================
# CHÂN TRANG
# ============================================================

st.divider()

st.caption(
    "💰 Financial Goal Planner | "
    "Công cụ mô phỏng kế hoạch tiết kiệm cá nhân"
)

st.caption(
    "⚠️ Kết quả chỉ mang tính chất tham khảo. "
    "Lãi suất thực tế, cách nhập lãi và thời điểm gửi tiền "
    "có thể khác với mô hình mô phỏng."
)

import streamlit as st

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Máy tính lãi tiền gửi tiết kiệm")
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

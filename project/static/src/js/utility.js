function setAlert(message, alertType) {
  // required import <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  Swal.fire({
    title: message,
    icon: alertType,
    confirmButtonText: "Okay",
  });
}

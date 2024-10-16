function setAlert(message, alertType) {
  // required import <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
  Swal.fire({
    title: message,
    icon: alertType,
    confirmButtonText: "Okay",
  });
}
function confirmAction(message, alertType, actionCallback) {
  Swal.fire({
    title: message,
    icon: alertType,
    showCancelButton: true,
    confirmButtonText: "Yes, do it!",
    cancelButtonText: "Cancel",
  }).then((result) => {
    if (result.isConfirmed) {
      actionCallback();
    }
  });
}

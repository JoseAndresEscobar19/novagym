var callbacks = callbacks || {};

function doPost(event) {
  event.preventDefault();
  let url = $(this).data('url');
  let data = $(this).serializeArray();
  $.ajax({
    url: url,
    type: 'POST',
    data: data,
    success: (res) => {
      $('.go-back', this).trigger('click');
      callbacks.success(res);
    },
    error: (error) => {
      console.error(error);
      callbacks.errors(error);
    },
  });
}

function openModelWithContext(event) {
  var $this = $(this);
  var target = $this.data('target');
  var type = $this.data('type');
  var url;
  var callback;
  switch (type) {
    case 'checkbox':
      var url_activar = $this.data('url-activar');
      var url_eliminar = $this.data('url-eliminar');
      url = $this.is(':checked') ? url_activar : url_eliminar;
      callback = () => {
        let return_og = $(this).is(':checked') ? 'off' : 'on';
        $(this).bootstrapToggle(return_og, true);
      };
      break;
    default:
      url = $this.data('url');
      break;
  }

  $.ajax({
    url: url,
    success: function (data) {
      $(target + ' .modal-content').html(data);
      $(target).modal('show');
    },
  });

  $(target).on('hide.bs.modal', callback);
}

$(document).on('click change', '.use-modal', openModelWithContext);
$(document).on('submit', '.do-post', doPost);

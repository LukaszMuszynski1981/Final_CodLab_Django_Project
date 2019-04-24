$('#reservation_form').trigger("reset");
$("#id_arrive, #id_departure").addClass("jquery-datepicker__input");
$("#id_meal option:nth-child(1),#id_instructor option:nth-child(1)").html("--");
$(".table_reservation_form_3 td:nth-child(4), .table_reservation_form_3 td:nth-child(6)").css(
    {"padding-left": "0px"});
$divOne = $("div.div_reservation_form:eq(1)");
$divTwo = $("div.div_reservation_form:eq(2)");
$divThree = $("div.div_reservation_form:eq(3)");


function jsValidateForm() {
    var $arrDate = $("#id_arrive").val();
    var $depDate = $('#id_departure').val();

    if ($arrDate >= $depDate) {
        alert("Data wyjazdu musi być późniejsza");
        return false
    } else {
        $.ajax({
            url: "/reservation",
            data: {
                arriveDate: $arrDate,
                departureDate: $depDate,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            type: "POST",
            dataType: "json"
        })
            .done(function(data) {
                var $dis = data.notAvailableRooms;
                $('#id_room option').each(function() {
                    var $inter_this = $(this);
                    $inter_this.prop('disabled', false);
                    $.each($dis,function(index,value){
                        if(index === $inter_this.val() && value === 'not available') {
                            $inter_this.prop('disabled', true);
                        }
                    });
                });
            })
            .fail(function () {
                console.log(
                    'wrong'
                )
            });
        $divOne.removeClass('hidden');
    }

}


function jsDeleteReservation() {
    if(confirm("Czy napewno chcesz skasować rezerwację? Tej operacji nie można cofnąć")){
        $.ajax({
            data: {
                url: "/my-reservation",
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            type: "POST",
            dataType: "json"

        }).done(function(data){
            if(data.redirect === 'true'){
                window.location.href = data.redirect_url;
            }
        }).fail(function(){
            alert("Nie możemy wykasować rezerwacji.")
        })
    } else {
        return false
    }
}


function jsReturnPrice() {
    var $room = $("#id_room").val();
    var $arrDate = $("#id_arrive").val();
    var $depDate = $('#id_departure').val();
    $.ajax({
      data: {
          url: "/reservation",
          requested_type: $room,
          arriveDate: $arrDate,
          departureDate: $depDate,
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
      },
      type: "GET",
      dataType: "json"

    }).done(function(data){
        $("#total_room_price").text("Koszt pokoju za cały pobyt: " + data.price + "Pln");
        $("#total_meal_price").text("Koszt posiłków za cały pobyt: " + data.meal + "Pln");
        $("#instructor_price_per_day").text("Koszt instruktora za dzień: " + data.instructor + "Pln");
    }).fail(function(){
        console.log('Błąd', data)
    })

}


$(document).ready(function(){

    $("#reservation_button_one").on('click', function(event) {
        if ($("#id_room").val() === '0') {
            event.preventDefault();
            alert('Proszę wybrać rodzaj pokoju');
            return false
        }
    });

    $("#reservation_button_two").on('click', function(event){
        if ($("#id_room").val() === '0') {
            event.preventDefault();
            alert('Proszę wybrać rodzaj pokoju');
            return false
        }
        if ($("#id_instructors").val() === '0'){
            event.preventDefault();
            alert('Proszę wybrać instruktora');
            return false
        }
    });

    $("#id_meal").change(function(){
       if(this.value === '2') {
           $("#total_meal_price").removeClass('hidden')
       } else {
           $("#total_meal_price").addClass('hidden')
       }
    });

    $("#id_room").change(function(){
       if(this.value === '0') {
           $("#total_room_price").addClass('hidden')
       }
       if(this.value !== '0') {
           $("#total_room_price").removeClass('hidden')
       }
    });

    $("#id-arrive").change(function(){
        $('#reservation_form').trigger("reset");
        $divOne.toggleClass('hidden');
    });

    $("#id_instructor").change(function(){
        if (this.value === '2') {
            $("#instructor_price_per_day").removeClass('hidden');
            $divTwo.removeClass('hidden');
            $("#reservation_button_two").removeClass('hidden');
            $("#reservation_button_one").addClass('hidden');
            $("#id_i_name, #id_child, #id_adult").prop('required', true);
        } else {
            $divTwo.addClass('hidden');
            $("#instructor_price_per_day").addClass('hidden');
            $("#reservation_button_two").addClass('hidden');
            $("#reservation_button_one").removeClass('hidden')
        }
    });

    $("#id_child, #id_child_two, #id_child_three").change(function() {
        if (this.checked) {
            switch_next_disable($(this))
        } else {
            switch_next_enable($(this))
        }
    });

    $("#id_adult, #id_adult_two, #id_adult_three").change(function() {
        if (this.checked) {
            switch_prev_disable($(this))
        } else {
            switch_prev_enable($(this))
        }

    });

    var $adult = $('#adult').text();
    var $child = $('#child').text();

    if($adult === 'True'){
        $('#adult').text('Tak')
    } else {
        $('#adult').text('Nie')
    }
    if($child === 'True'){
        $('#child').text('Tak')
    } else {
        $('#child').text('Nie')
    }

    function switch_next_disable(param) {
        param.parent().next().next().children().prop('disabled', true);
        param.parent().next().next().children().prop('required', false);
    }

    function switch_next_enable(param) {
        param.parent().next().next().children().prop('disabled', false);
        param.parent().next().next().children().prop('required', true);
    }

    function switch_prev_disable(param) {
        param.parent().prev().prev().children().prop('disabled', true);
        param.parent().prev().prev().children().prop('required', false);
    }

    function switch_prev_enable(param) {
        param.parent().prev().prev().children().prop('disabled', false);
        param.parent().prev().prev().children().prop('required', true);
    }
});





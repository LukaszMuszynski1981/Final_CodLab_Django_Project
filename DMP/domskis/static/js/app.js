$("#id_arrive, #id_departure").addClass("jquery-datepicker__input");
$("#id_meal option:nth-child(1),#id_instructor option:nth-child(1)").html("--");
$(".table_reservation_form_three td:nth-child(4), .table_reservation_form_three td:nth-child(6)").css(
    {"padding-left": "0px"});
$divOne = $("div.div_reservation_form:eq(1)");
$divTwo = $("div.div_reservation_form:eq(2)");
$divThree = $("div.div_reservation_form:eq(3)");


function jsValidateForm(){

    var $arrDate = $("#id_arrive").val();
    var $depDate = $('#id_departure').val();

    if ($arrDate >= $depDate) {
        alert("Data wyjazdu musi być późniejsza");
        $("#id_arrive").val(datepicker);
        return false

    } else {
        $.ajax({
            url: "/reservation",
            data: {
                arriveDate: $arrDate,
                departureDate: $depDate,
                what: 'dateTocheck',
            },
            type: "GET",
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
                $divOne.removeClass("hidden");
            })
            .fail(function (data) {
                console.log(
                    "wrong", data
                );
            });
        }
    }


function jsDeleteReservation(){

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


function jsReturnPrice(){

    var $room = $("#id_room").val();
    var $arrDate = $("#id_arrive").val();
    var $depDate = $('#id_departure').val();

    $.ajax({
            url: "/reservation",
            data: {
              requested_type: $room,
              arriveDate: $arrDate,
              departureDate: $depDate,
              what: 'requestedRoom',
            },
            type: "GET",
            dataType: "json"

        }).done(function(data){

            $("#total_room_price").text("Koszt pokoju za cały pobyt: " + data.price + "Pln");
            $("#total_meal_price").text("Koszt posiłków za cały pobyt: " + data.meal + "Pln");
            $("#instructor_price_per_day").text("Koszt instruktora za dzień: " + data.instructor + "Pln");

        }).fail(function(data){

            console.log('Błąd', data)
        })

    }


function jsValidateRoom(){

    if ($("#id_room").val() === '0') {
        event.preventDefault();
        alert('Proszę wybrać rodzaj pokoju');
        return false
    }
}


$(document).ready(function(){

    $("#id_arrive").change(function(){
        var $classList = $("div.div_reservation_form:eq(1)").attr("class").split(/\s+/);
        if(jQuery.inArray("hidden", $classList) ===  -1) {
            jsValidateForm()
        }
    });

    $("#id_departure").change(function(){
        jsValidateForm();
        $("#id_room").val("0");
    });

    $("#reservation_button_one").on('click', function(){
        jsValidateRoom();
    });

    $("#reservation_button_two").on('click', function(){
        jsValidateRoom();
        if ($("#id_instructors_one").val() === '0'){
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

    $("#id_instructor").change(function(){
        if (this.value === '2') {
            $("#instructor_price_per_day, #reservation_button_two").removeClass('hidden');
            $divTwo.removeClass('hidden');
            $("#reservation_button_one").addClass('hidden');
            $("#id_i_name_one, #id_child_one, #id_adult_one").prop('required', true);
        } else {
            $divTwo.addClass('hidden');
            $("#instructor_price_per_day, #reservation_button_two").addClass('hidden');
            $("#reservation_button_one").removeClass('hidden')
        }
    });


    $("#id_child_one, #id_child_two, #id_child_three, #id_adult_one, #id_adult_two, #id_adult_three").change(function() {

        var $indicator = $(this).attr("id");
        if ($indicator.includes("child")) {
            var temp = $indicator.replace("child", "adult");
            if ($indicator === "id_child_one") {
                if (this.checked) {
                    $("#" + temp).prop("disabled", true, "required", false);
                } else {
                    $("#" + temp).prop("disabled", false, "required", true);
                }
            } else {
                var tempTwo = $indicator.replace("child", "i_name");
                if (this.checked) {
                    $("#" + temp).prop("disabled", true, "required", false);
                    $("#" + tempTwo).prop("required", true);
                } else {
                    $("#" + temp).prop("disabled", false, "required", false);
                    $("#" + tempTwo).prop("required", false);
                }
            }
        } else {
            var temp = $indicator.replace("adult", "child");
            if ($indicator === "id_adult_one") {
                if (this.checked) {
                    $("#" + temp).prop("disabled", true, "required", false);
                } else {
                    $("#" + temp).prop("disabled", false, "required", true);
                }
            } else {
                var tempTwo = $indicator.replace("adult", "i_name");
                if (this.checked) {
                    $("#" + temp).prop("disabled", true, "required", false);
                    $("#" + tempTwo).prop("required", true);
                } else {
                    $("#" + temp).prop("disabled", false, "required", false);
                    $("#" + tempTwo).prop("required", false);
                }
            }

        }
    });


    $(".adult, .child").each(function () {
        var $inner_text = $(this).text();
        if ($inner_text === "True") {
            $(this).text("Tak")
        } else {
            $(this).text("Nie")
        }
    });

    $("#upload_redirection").on("click", function() {
        $("input[type=file]").click()
    });

});





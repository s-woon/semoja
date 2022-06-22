// 화면이 전부 로딩이 완료되었다면, 함수안의 기능 불러오기
$(document).ready(function () {
    get_certificate_detail()
})

// 상단 자격증 select 코드 구현
function select_certificate_division() {

}

// 자격증 상세정보 - mongoDB 불러오기
function get_certificate_detail() {
    $.ajax({
        type:"GET",
        url:"/certificateDetails/get_detail",
        data:{},
        success: function (response) {
            rows = response["certificate_detail"]
            console.log(rows)
            let division = ""
            let implNm = ""
            let index = ""
            let instiNm = ""
            let jmNm = ""
            let mdobligFldNm = ""
            let summary = ""
            let temp_html = ""
            let summary_html = ""
            for (let i = 0; i < rows.length; i++) {
                implNm = rows[i]["implNm"]
                index = rows[i]["index"]
                instiNm = rows[i]["instiNm"]
                jmNm = rows[i]["jmNm"]
                mdobligFldNm = rows[i]["mdobligFldNm"]
                summary = rows[i]["summary"]
                if (index === 1) {
                    division = "기술사"
                } else if (index === 2) {
                    division = "기능장"
                } else if (index === 3) {
                    division = "기사"
                } else if (index === 4) {
                    division = "기능사"
                }
                temp_html = `
                    <li>구분 : ${division} </li>
                    <li>자격명 : ${jmNm} </li>
                    <li>직종 : ${mdobligFldNm} </li>
                    <li>시행기관 : ${implNm}</li>
                    <li>관련부처 : ${instiNm} </li>                    
                `
                summary_html = `
                    <p>${summary}</p>
                `
                // $('#certificate_detail').append(temp_html)
            }
            $('#certificate_ul').append(temp_html)
            $("#summary").append(summary_html)
        }
    })
}

// 코멘트 입력 버튼 구현
function toggle_comment_button() {
    $("#comment").toggle('slow');
    if($("#comment_toggle").val() == 0) {
        $("#comment_toggle").text("코멘트 입력 숨기기")
        $("#comment_toggle").val(1)
    } else {
        $("#comment_toggle").text("코멘트 입력")
        $("#comment_toggle").val(0)
    }
}

// 자격증 코멘드 남기기 버튼 구현
function save_comment() {
    let comment = $("#comment_textarea").val()
    $.ajax({
        type:"POST",
        url:'/certificateDetails/post_comment',
        data:{
            comment_give:comment
        },
        success:function (response) {
            alert(response['msg'])
            window.location.reload()
        }
    })
}
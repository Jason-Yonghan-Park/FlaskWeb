<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<script>
$(function() {
	$("#btnFlask").click(function() {
		console.log("btnFlask Clicked...");
		$.ajax({
			url:"http://127.0.0.1:9000/mListJson",
			type: "post",
			data: { "no":  1},
			success: function(res) {
				console.log(res.length);
				//res = eval("(" + res + ")")
				
				$("#result").append("<table id='resultTable'></table>");
				var th = "<tr>"
						+ "<th> no </th>"
						+ "<th> id </th>"
						+ "<th> 이름 </th>"
						+ "<th> email </th>"
						+ "<th> 주소 </th>"
						"</tr>";
				$("#resultTable").append(th);
				
				//{"address1": "서울 마포구 노고산동 11", "email": "midas@naver.com", "id": "midastop111", "name": "홍길삼", "no": 4, "phone": "010-8917-6683", "pw": "1234", "regDate": "2020-05-12T11:39:18"}
				$.each(res, function(i, v) {
					var tr = "<tr>"
							+ "<td>" + v.no + "</td>"
							+ "<td>" + v.id + "</td>"
							+ "<td>" + v.name + "</td>"
							+ "<td>" + this.email + "</td>"
							+ "<td>" + this.address1 + "</td>"
						"</tr>";
					$("#resultTable").append(tr);
				});
				
			},
			error: function(xhr, statusText, err) {
				console.log(statusText + " == " + err);
			}	
		});
	});	
});
</script>    
<article>
	<h1>Flask 연동하기</h1>
	<button id="btnFlask">Flask에서 회원 리스트 가져오기</button>
	<div id="result">	
	</div>
</article>

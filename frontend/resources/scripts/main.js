//  src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js">

// $(document).ready(function(){
//     $.ajax({
//         url: '/your_protected_route',
//         type: 'GET',
//         success: function(data) {
//             // Handle successful response
//         },
//         error: function(response) {
//             if(response.status == 401) { // Unauthorized
//                 alert("You cannot perform this action until you are logged in");
//                 // Or update the HTML content
//                 // $('#notification').text("You cannot perform this action until you are logged in");
//             }
//         }
//     });
// });


const logout = () => {
    sessionStorage.setItem("access_token", "")
}

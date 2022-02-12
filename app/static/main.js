// // static/main.js

// console.log("Sanity check!");

// // Get Stripe publishable key
// fetch("/config")
// .then((result) => { return result.json(); })
// .then((data) => {
//   // Initialize Stripe.js
//   const stripe = Stripe(data.publicKey);

//   // new
//   // Event handler
//   document.querySelectorAll(".checkoutBtn").forEach((button) => {
//       button.addEventListener("click", () => {
//       // Get Checkout Session ID
//       fetch("/my-requests/cart/checkout")
//       .then((result) => { return result.json(); })
//       .then((data) => {
//         console.log(data);
//         // Redirect to Stripe Checkout
//         return stripe.redirectToCheckout({sessionId: data.sessionId})
//       })
//       .then((res) => {
//         console.log(res);
//       });
//     });
//   });
//   })
function myFunction() {
    var coll = document.getElementById("collapse");
    var content = coll.nextElementSibling;

    // Toggle the "active" class for the button (if you have styles for it)
    coll.classList.toggle("active");

    // Toggle the display property of the content
    if (content.style.display === "block") { // When content is hidden
        content.style.display = "none";
        coll.style.marginBottom = "20px"; // Have gap below button
    } else { // When content is visible
        content.style.display = "block";
        coll.style.marginBottom = "0"; // Remove gap so that the filters are directly under the button. The marginBottom of the content will create the gap between the song list.
    }
}
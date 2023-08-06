function number_examples() {
    var examples = document.querySelectorAll("li.example");
    for (var exc = 0; exc < examples.length; exc++) {
        ex = examples[exc]
        ex.setAttribute("value", exc + 1)
    }
}
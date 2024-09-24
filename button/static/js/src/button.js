function ButtonXBlock(runtime, element) {
    // For students: Handle evaluation
    $(element).find('#evaluate-button').click(function() {
        var answer = $(element).find('#student-answer').val();
        
        $.ajax({
            type: 'POST',
            url: runtime.handlerUrl(element, 'evaluate_answer'),
            data: JSON.stringify({ answer: answer }),
            success: function(response) {
                var resultText = "Problem: " + response.problem + "<br>" +
                                 "Your Answer: " + response.answer + "<br>" + 
                                 "Your Evaluation: " + response.evaluation;
                $(element).find('#evaluation-result').html(resultText);
            }
        });
    });

    // For instructors: Handle save of problem and rubric
    $(element).find('#save-button').click(function() {
        var problemDescription = $(element).find('#problem-description').val();
        var rubric = $(element).find('#rubric').val();
        
        $.ajax({
            type: 'POST',
            url: runtime.handlerUrl(element, 'save_problem_and_rubric'),
            data: JSON.stringify({
                problem_description: problemDescription,
                rubric: rubric
            }),
            success: function(response) {
                alert("Problem and rubric saved successfully!");
            }
        });
    });
}


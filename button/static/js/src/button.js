function ButtonXBlock(runtime, element) {
    // Add a new rubric section
    $(element).find('#add-section').click(function() {
        $('#rubric-sections').append(`
            <div class="rubric-section">
                <label>Label:</label>
                <input type="text" value="Enter label here" class="rubric-label" />
                <textarea rows="2" cols="50" class="rubric-text"></textarea>
                <button class="remove-section">Remove</button>
            </div>
        `);
    });

    // Remove a rubric section
    $(element).on('click', '.remove-section', function() {
        if ($('.rubric-section').length > 2) {
            $(this).parent().remove();
        }
    });

    // Save rubric and problem description
    $(element).find('#save-button').click(function() {
        var problemDescription = $(element).find('#problem-description').val();
        
        var rubricSections = [];
        $('.rubric-section').each(function() {
            var label = $(this).find('.rubric-label').val();
            var text = $(this).find('.rubric-text').val();
            rubricSections.push({ label: label, text: text });
        });

        $.ajax({
            type: 'POST',
            url: runtime.handlerUrl(element, 'save_problem_and_rubric'),
            data: JSON.stringify({
                problem_description: problemDescription,
                rubric_sections: rubricSections
            }),
            success: function(response) {
                alert("Problem and rubric saved successfully!");
            }
        });
    });
}


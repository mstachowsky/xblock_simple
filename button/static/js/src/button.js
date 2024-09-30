function ButtonXBlock(runtime, element) {
    // Function to add a new rubric section
    function addRubricSection() {
        var newSection = `
            <div class="rubric-section">
                <label>Enter label here:</label>
                <input type="text" class="rubric-label" value="Enter label here">
                <textarea class="rubric-option" rows="2" cols="50">Enter rubric text</textarea>
                <button class="remove-section-button">Remove</button>
            </div>`;
        $(element).find('#rubric-sections').append(newSection);
    }

    // Ensure there are at least 2 sections
    function enforceMinimumSections() {
        var sections = $(element).find('.rubric-section');
        if (sections.length <= 2) {
            $(sections).find('.remove-section-button').hide();
        } else {
            $(sections).find('.remove-section-button').show();
        }
    }

    // Handle removing a section
    $(element).on('click', '.remove-section-button', function() {
        $(this).closest('.rubric-section').remove();
        enforceMinimumSections();
    });

    // Add a new rubric section when the button is clicked
    $(element).find('#add-section-button').click(function() {
        addRubricSection();
        enforceMinimumSections();
    });

    // For instructors: Handle save of problem and rubric
    $(element).find('#save-button').click(function() {
        var problemDescription = $(element).find('#problem-description').val();
        
        // Gather all rubric sections into a single string
        var rubricSections = [];
        $(element).find('.rubric-section').each(function() {
            var label = $(this).find('.rubric-label').val();
            var text = $(this).find('.rubric-option').val();
            rubricSections.push(label + ": " + text);
        });
        var rubric = rubricSections.join("\n");

        // Send the data to the server
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

    // Initial enforcement of minimum sections
    enforceMinimumSections();
}


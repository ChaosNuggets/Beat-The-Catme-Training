<!DOCTYPE html>
<html>
<head>
    <title>Beat The Catme Training</title>
</head>
<body>

    <h1>Beat The Catme Training</h1>

    <?php
        // Calculate the answers
        $output = shell_exec("input_descriptions_as_args.py \"" . $_POST["d1"] . "\" \"" . $_POST["d2"] . "\" \"" . $_POST["d3"] . "\"");
        $answers = explode("\n", $output);

        // Check if there was an error (maybe the user didn't enter anything or entered something invalid)
        if (count($answers) < 5)
        {
            echo $output . '<br><br>';
            echo '<a href="index.html">Try again</a>';
            exit;
        }

        // Print the answers
        for ($i = 0; $i < count($answers); $i++)
        {
            echo '<h2>Question ' . $i + 1 . ':</h2>';
            echo $answers[$i];
        }
        
    ?><br><br><br>

    <a href="index.html">
        Enter more descriptions
    </a>

</body>
</html> 
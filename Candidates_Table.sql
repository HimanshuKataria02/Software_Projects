CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(30) NOT NULL,
    college_name VARCHAR(50) NOT NULL,
    round_one_marks FLOAT CHECK (round_one_marks BETWEEN 0 AND 10),
    round_two_marks FLOAT CHECK (round_two_marks BETWEEN 0 AND 10),
    round_three_marks FLOAT CHECK (round_three_marks BETWEEN 0 AND 10),
    technical_round_marks FLOAT CHECK (technical_round_marks BETWEEN 0 AND 20),
    total_marks FLOAT GENERATED ALWAYS AS (round_one_marks + round_two_marks + round_three_marks + technical_round_marks) STORED,
    result VARCHAR(10) GENERATED ALWAYS AS (CASE WHEN total_marks >= 35 THEN 'Selected' ELSE 'Rejected' END) STORED,
    `rank` INT
);

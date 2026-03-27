export const exercises_data = [
    {
        type: 'squat',
        image: '/image/squat.jpg',
        difficulty: 'Beginner',
        rating: 95,
        title: 'Squats',
        hasEquipment: false, // Bodyweight
        description: 'Bài tập hạ thấp người như động tác ngồi xuống rồi đứng lên, tập trung vào đùi, mông và cơ core, rất hiệu quả cho sức mạnh phần thân dưới.',
        time: '10-15',
        kcal: 120,
        muscles: ['Quadriceps', 'Glutes'],
        steps: [
            'Đứng thẳng, hai chân rộng bằng vai.',
            'Hạ thấp hông xuống như thể bạn đang ngồi vào một chiếc ghế ẩn.',
            'Giữ lưng thẳng và đảm bảo đầu gối không vượt quá mũi chân.',
            'Dùng lực gót chân để đẩy người đứng dậy về vị trí ban đầu.'
        ],
        tips: [
            "Giữ lưng thẳng, không để cong lưng",
            "Dồn trọng tâm vào gót chân",
            "Hạ mông xuống thấp nhất có thể",
            "Đừng để đầu gối quá mũi chân",
            "Hít vào khi xuống, thở ra khi lên"
        ],
        proTip: 'Hít vào khi hạ người xuống và thở ra mạnh khi đẩy người lên để tối ưu sức mạnh và giữ ổn định cơ lõi.',
        damege: 30
    },
    {
        type: 'pushup',
        image: '/image/pushups.jpg',
        difficulty: 'Beginner',
        rating: 92,
        title: 'Push-ups',
        hasEquipment: false, // Bodyweight
        description: 'Bài tập chống đẩy, dùng tay đẩy cơ thể lên xuống khỏi mặt đất, giúp phát triển ngực, vai, tay sau và core.',
        time: '5-10',
        kcal: 95,
        muscles: ['Chest', 'Triceps'],
        steps: [
            "Giữ cơ thể thành một đường thẳng",
            "Không để mông quá cao hoặc quá thấp",
            "Mở rộng ngực khi hạ người xuống",
            "Gồng chặt cơ bụng khi thực hiện",
            "Khuỷu tay khép vào gần thân người"
        ],
        tips: [
            "Giữ lưng thẳng, không để cong lưng",
            "Dồn trọng tâm vào gót chân",
            "Hạ mông xuống thấp nhất có thể",
            "Đừng để đầu gối quá mũi chân",
            "Hít vào khi xuống, thở ra khi lên"
        ],
        proTip: 'Giữ cơ bụng siết chặt và không để hông võng để tránh chấn thương lưng.',
        damege: 30,
    },
    {
        type: 'plank',
        image: '/image/plank.jpg',
        difficulty: 'Beginner',
        rating: 92,
        title: 'Plank',
        hasEquipment: false, // Bodyweight
        description: 'Bài tập giữ cơ thể thẳng như tấm ván, chống bằng khuỷu tay và mũi chân để tăng sức mạnh cơ core (bụng, lưng dưới) và cải thiện khả năng giữ thăng bằng.',
        time: '5-10',
        kcal: 95,
        muscles: ['Chest', 'Triceps'],
        steps: [
            'Giữ cơ thể trên một đường thẳng từ đầu đến gót chân.',
            'Chống bằng khuỷu tay và mũi chân.',
            'Gồng chặt cơ bụng và giữ tư thế lâu nhất có thể.'
        ],
        tips: [
            "Giữ đầu, lưng, chân thẳng hàng",
            "Không nín thở, hãy hít thở đều",
            "Gồng chặt cơ bụng và cơ mông",
            "Mắt nhìn xuống sàn, đừng ngước lên",
            "Cố gắng giữ vững tư thế, đừng rung lắc"
        ],
        proTip: 'Giữ thân người thẳng và dồn lực vào gót chân trước để tăng hiệu quả tập luyện.',
        damege: 20
    },
    {
        type: 'lungue',
        image: '/image/lunge.jpg',
        difficulty: 'Advanced',
        rating: 85,
        title: 'Lunges',
        hasEquipment: false, // Bodyweight
        description: 'Bài tập bước chân dài về phía trước hoặc sau rồi hạ thấp người, giúp tăng sức mạnh đùi trước, đùi sau và mông, đồng thời cải thiện thăng bằng.',
        time: '10-12',
        kcal: 85,
        muscles: ['Quadriceps', 'Glutes'],
        steps: [
            'Đứng thẳng, hai chân rộng bằng vai.',
            'Bước một chân lên phía trước và hạ thấp hông.',
            'Đảm bảo đầu gối chân trước tạo góc 90 độ.',
            'Dùng lực chân trước để đẩy người về vị trí ban đầu.'
        ],
        tips: [
            "Giữ lưng thẳng, mắt nhìn về phía trước",
            "Bước chân đủ dài để tạo góc 90° ở đầu gối",
            "Đầu gối chân trước không vượt quá mũi chân",
            "Hạ người xuống từ từ, giữ thăng bằng cơ thể",
            "Dùng lực chân trước để đẩy người trở lại vị trí ban đầu"
        ],
        proTip: 'Hít vào khi hạ người xuống và thở ra mạnh khi đẩy người lên để tối ưu sức mạnh cốt lõi.',
        damege: 30
    },
    {
        type: "bicep_curls",
        image: "/image/bicep_curls.jpg",
        difficulty: "Beginner",
        rating: 80,
        title: "Bicep Curls",
        hasEquipment: true, // Cần tạ (Dumbbell/Barbell)
        description: "Bài tập cô lập tập trung vào nhóm cơ bắp tay trước, giúp tăng kích thước và sức mạnh cánh tay.",
        time: "12-15",
        kcal: 65,
        muscles: ["Biceps", "Forearms"],
        steps: [
            "Đứng thẳng, hai tay cầm tạ buông dọc thân người.",
            "Giữ khuỷu tay cố định sát hông, từ từ cuốn cánh tay dưới lên phía vai.",
            "Siết chặt cơ bắp tay ở vị trí cao nhất trong 1 giây.",
            "Từ từ hạ tay về vị trí ban đầu theo kiểm soát."
        ],
        tips: [
            "Giữ khuỷu tay cố định, không vung vẩy cánh tay trên",
            "Không dùng đà từ lưng hoặc vai để đưa tay lên",
            "Mở rộng biên độ chuyển động hết mức (full range of motion)",
            "Giữ cổ tay thẳng, không gập cổ tay khi cuốn"
        ],
        proTip: "Siết chặt bắp tay ở đỉnh động tác và hạ xuống chậm gấp đôi khi đưa lên để xé nhỏ sợi cơ.",
        damage: 25
    },
    {
        type: "shoulder_press",
        image: "/image/shoulder_press.jpg",
        difficulty: "Intermediate",
        rating: 90,
        title: "Shoulder Press",
        hasEquipment: true,
        description: "Bài tập đẩy tạ qua đầu giúp phát triển toàn diện cơ vai, cơ tam đầu (tay sau) và cải thiện sức mạnh thân trên.",
        time: "10-12",
        kcal: 95,
        muscles: ["Deltoids", "Triceps"],
        steps: [
            "Đứng thẳng hoặc ngồi, giữ tạ ở ngang tầm vai.",
            "Siết cơ bụng, đẩy tạ thẳng lên trên cho đến khi cánh tay duỗi thẳng qua đầu.",
            "Dừng lại một chút ở đỉnh, tránh để tạ chạm vào nhau.",
            "Hạ tạ xuống từ từ về lại vị trí ngang vai."
        ],
        tips: [
            "Không khóa khớp khuỷu tay hoàn toàn ở vị trí cao nhất",
            "Giữ lưng thẳng, không được võng lưng dưới khi đẩy nặng",
            "Kiểm soát tạ khi hạ xuống, không để tạ rơi tự do",
            "Cùi chỏ hơi hướng về phía trước khoảng 30 độ để bảo vệ khớp vai"
        ],
        proTip: "Tưởng tượng bạn đang đẩy trần nhà lên cao để kích hoạt tối đa nhóm cơ vai.",
        damage: 45
    }
];
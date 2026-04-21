const textbookData = {
  grades: [
    { id: 'g3', name: '三年级', emoji: '🌱' },
    { id: 'g4', name: '四年级', emoji: '🌿' },
    { id: 'g5', name: '五年级', emoji: '🌳' },
    { id: 'g6', name: '六年级', emoji: '🌲' }
  ],
  volumes: [
    { id: 'v1', name: '上册', emoji: '📗' },
    { id: 'v2', name: '下册', emoji: '📕' }
  ],
  units: {
    g3_v1: [
      {
        id: 'u1', name: 'Unit 1 Hello!', emoji: '👋',
        words: [
          { en: 'hello', phonetic: '/həˈləʊ/', cn: '你好' },
          { en: 'hi', phonetic: '/haɪ/', cn: '嗨' },
          { en: 'I', phonetic: '/aɪ/', cn: '我' },
          { en: 'am', phonetic: '/æm/', cn: '是' },
          { en: 'goodbye', phonetic: '/ɡʊdˈbaɪ/', cn: '再见' },
          { en: 'bye', phonetic: '/baɪ/', cn: '拜拜' }
        ],
        sentences: [
          { en: 'Hello, I\'m Mike.', cn: '你好，我是迈克。' },
          { en: 'Hi, I\'m Sarah.', cn: '嗨，我是萨拉。' },
          { en: 'Goodbye!', cn: '再见！' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Hello, I\'m Wu Yifan.', cn: '你好，我是吴一凡。' },
          { speaker: 'B', avatar: 'b', en: 'Hi, I\'m Sarah.', cn: '嗨，我是萨拉。' }
        ]
      },
      {
        id: 'u2', name: 'Unit 2 Colours', emoji: '🎨',
        words: [
          { en: 'red', phonetic: '/red/', cn: '红色' },
          { en: 'yellow', phonetic: '/ˈjeləʊ/', cn: '黄色' },
          { en: 'green', phonetic: '/ɡriːn/', cn: '绿色' },
          { en: 'blue', phonetic: '/bluː/', cn: '蓝色' },
          { en: 'black', phonetic: '/blæk/', cn: '黑色' },
          { en: 'white', phonetic: '/waɪt/', cn: '白色' }
        ],
        sentences: [
          { en: 'I see red.', cn: '我看见红色。' },
          { en: 'I see green.', cn: '我看见绿色。' },
          { en: 'Show me green.', cn: '给我看看绿色。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Mr Jones, this is Miss Green.', cn: '琼斯先生，这是格林小姐。' },
          { speaker: 'B', avatar: 'b', en: 'Nice to meet you.', cn: '很高兴见到你。' }
        ]
      },
      {
        id: 'u3', name: 'Unit 3 Look at me!', emoji: '👀',
        words: [
          { en: 'face', phonetic: '/feɪs/', cn: '脸' },
          { en: 'ear', phonetic: '/ɪə(r)/', cn: '耳朵' },
          { en: 'eye', phonetic: '/aɪ/', cn: '眼睛' },
          { en: 'nose', phonetic: '/nəʊz/', cn: '鼻子' },
          { en: 'mouth', phonetic: '/maʊθ/', cn: '嘴巴' },
          { en: 'arm', phonetic: '/ɑːm/', cn: '手臂' }
        ],
        sentences: [
          { en: 'Close your eyes.', cn: '闭上你的眼睛。' },
          { en: 'Open your mouth.', cn: '张开你的嘴巴。' },
          { en: 'Touch your nose.', cn: '摸摸你的鼻子。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Look at me!', cn: '看看我！' },
          { speaker: 'B', avatar: 'b', en: 'This is my face.', cn: '这是我的脸。' }
        ]
      },
      {
        id: 'u4', name: 'Unit 4 We love animals', emoji: '🐾',
        words: [
          { en: 'duck', phonetic: '/dʌk/', cn: '鸭子' },
          { en: 'pig', phonetic: '/pɪɡ/', cn: '猪' },
          { en: 'cat', phonetic: '/kæt/', cn: '猫' },
          { en: 'bear', phonetic: '/beə(r)/', cn: '熊' },
          { en: 'dog', phonetic: '/dɒɡ/', cn: '狗' },
          { en: 'bird', phonetic: '/bɜːd/', cn: '鸟' }
        ],
        sentences: [
          { en: 'What\'s this?', cn: '这是什么？' },
          { en: 'It\'s a duck.', cn: '它是一只鸭子。' },
          { en: 'Act like a bird.', cn: '模仿一只鸟。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'What\'s this?', cn: '这是什么？' },
          { speaker: 'B', avatar: 'b', en: 'It\'s a bear.', cn: '它是一只熊。' }
        ]
      },
      {
        id: 'u5', name: 'Unit 5 Let\'s eat!', emoji: '🍔',
        words: [
          { en: 'bread', phonetic: '/bred/', cn: '面包' },
          { en: 'cake', phonetic: '/keɪk/', cn: '蛋糕' },
          { en: 'water', phonetic: '/ˈwɔːtə(r)/', cn: '水' },
          { en: 'milk', phonetic: '/mɪlk/', cn: '牛奶' },
          { en: 'egg', phonetic: '/eɡ/', cn: '鸡蛋' },
          { en: 'juice', phonetic: '/dʒuːs/', cn: '果汁' }
        ],
        sentences: [
          { en: 'I\'d like some juice, please.', cn: '请给我一些果汁。' },
          { en: 'Have some bread.', cn: '吃点面包吧。' },
          { en: 'Thank you.', cn: '谢谢你。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Mum, I\'m hungry!', cn: '妈妈，我饿了！' },
          { speaker: 'B', avatar: 'b', en: 'Have some bread.', cn: '吃点面包吧。' }
        ]
      },
      {
        id: 'u6', name: 'Unit 6 Happy birthday!', emoji: '🎂',
        words: [
          { en: 'one', phonetic: '/wʌn/', cn: '一' },
          { en: 'two', phonetic: '/tuː/', cn: '二' },
          { en: 'three', phonetic: '/θriː/', cn: '三' },
          { en: 'four', phonetic: '/fɔː(r)/', cn: '四' },
          { en: 'five', phonetic: '/faɪv/', cn: '五' },
          { en: 'happy', phonetic: '/ˈhæpi/', cn: '快乐的' }
        ],
        sentences: [
          { en: 'Happy birthday!', cn: '生日快乐！' },
          { en: 'How old are you?', cn: '你多大了？' },
          { en: 'I\'m six years old.', cn: '我六岁了。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Happy birthday!', cn: '生日快乐！' },
          { speaker: 'B', avatar: 'b', en: 'Thank you!', cn: '谢谢！' }
        ]
      }
    ],
    g3_v2: [
      {
        id: 'u1', name: 'Unit 1 Welcome back!', emoji: '🏫',
        words: [
          { en: 'UK', phonetic: '/ˌjuː ˈkeɪ/', cn: '英国' },
          { en: 'Canada', phonetic: '/ˈkænədə/', cn: '加拿大' },
          { en: 'USA', phonetic: '/ˌjuː es ˈeɪ/', cn: '美国' },
          { en: 'China', phonetic: '/ˈtʃaɪnə/', cn: '中国' },
          { en: 'student', phonetic: '/ˈstjuːdnt/', cn: '学生' },
          { en: 'pupil', phonetic: '/ˈpjuːpl/', cn: '小学生' }
        ],
        sentences: [
          { en: 'I\'m from the UK.', cn: '我来自英国。' },
          { en: 'Welcome!', cn: '欢迎！' },
          { en: 'Nice to meet you.', cn: '很高兴见到你。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Hi, I\'m Amy.', cn: '嗨，我是艾米。' },
          { speaker: 'B', avatar: 'b', en: 'I\'m from the UK.', cn: '我来自英国。' }
        ]
      },
      {
        id: 'u2', name: 'Unit 2 My family', emoji: '👨‍👩‍👧',
        words: [
          { en: 'father', phonetic: '/ˈfɑːðə(r)/', cn: '父亲' },
          { en: 'mother', phonetic: '/ˈmʌðə(r)/', cn: '母亲' },
          { en: 'man', phonetic: '/mæn/', cn: '男人' },
          { en: 'woman', phonetic: '/ˈwʊmən/', cn: '女人' },
          { en: 'sister', phonetic: '/ˈsɪstə(r)/', cn: '姐妹' },
          { en: 'brother', phonetic: '/ˈbrʌðə(r)/', cn: '兄弟' }
        ],
        sentences: [
          { en: 'Who\'s that man?', cn: '那个男人是谁？' },
          { en: 'He\'s my father.', cn: '他是我的父亲。' },
          { en: 'Is she your mother?', cn: '她是你的母亲吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Who\'s that woman?', cn: '那个女人是谁？' },
          { speaker: 'B', avatar: 'b', en: 'She\'s my mother.', cn: '她是我的母亲。' }
        ]
      },
      {
        id: 'u3', name: 'Unit 3 At the zoo', emoji: '🦁',
        words: [
          { en: 'thin', phonetic: '/θɪn/', cn: '瘦的' },
          { en: 'fat', phonetic: '/fæt/', cn: '胖的' },
          { en: 'tall', phonetic: '/tɔːl/', cn: '高的' },
          { en: 'short', phonetic: '/ʃɔːt/', cn: '矮的；短的' },
          { en: 'long', phonetic: '/lɒŋ/', cn: '长的' },
          { en: 'small', phonetic: '/smɔːl/', cn: '小的' }
        ],
        sentences: [
          { en: 'Look at that giraffe.', cn: '看那只长颈鹿。' },
          { en: 'It\'s so tall!', cn: '它真高！' },
          { en: 'It has a long nose.', cn: '它有一个长鼻子。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Look at the elephant!', cn: '看那头大象！' },
          { speaker: 'B', avatar: 'b', en: 'It has a long nose.', cn: '它有一个长鼻子。' }
        ]
      },
      {
        id: 'u4', name: 'Unit 4 Where is my car?', emoji: '🚗',
        words: [
          { en: 'on', phonetic: '/ɒn/', cn: '在...上面' },
          { en: 'in', phonetic: '/ɪn/', cn: '在...里面' },
          { en: 'under', phonetic: '/ˈʌndə(r)/', cn: '在...下面' },
          { en: 'chair', phonetic: '/tʃeə(r)/', cn: '椅子' },
          { en: 'desk', phonetic: '/desk/', cn: '书桌' },
          { en: 'cap', phonetic: '/kæp/', cn: '帽子' }
        ],
        sentences: [
          { en: 'Where is my car?', cn: '我的小汽车在哪里？' },
          { en: 'It\'s under the chair.', cn: '它在椅子下面。' },
          { en: 'Silly me!', cn: '我真傻！' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Where is my pencil box?', cn: '我的铅笔盒在哪里？' },
          { speaker: 'B', avatar: 'b', en: 'It\'s in your desk.', cn: '它在你的书桌里。' }
        ]
      },
      {
        id: 'u5', name: 'Unit 5 Do you like pears?', emoji: '🍐',
        words: [
          { en: 'apple', phonetic: '/ˈæpl/', cn: '苹果' },
          { en: 'pear', phonetic: '/peə(r)/', cn: '梨' },
          { en: 'orange', phonetic: '/ˈɒrɪndʒ/', cn: '橙子' },
          { en: 'banana', phonetic: '/bəˈnɑːnə/', cn: '香蕉' },
          { en: 'watermelon', phonetic: '/ˈwɔːtəmelən/', cn: '西瓜' },
          { en: 'strawberry', phonetic: '/ˈstrɔːbəri/', cn: '草莓' }
        ],
        sentences: [
          { en: 'Do you like pears?', cn: '你喜欢梨吗？' },
          { en: 'Yes, I do.', cn: '是的，我喜欢。' },
          { en: 'No, I don\'t.', cn: '不，我不喜欢。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Do you like watermelons?', cn: '你喜欢西瓜吗？' },
          { speaker: 'B', avatar: 'b', en: 'Yes, I do. They\'re sweet!', cn: '是的，我喜欢。它们很甜！' }
        ]
      },
      {
        id: 'u6', name: 'Unit 6 How many?', emoji: '🔢',
        words: [
          { en: 'eleven', phonetic: '/ɪˈlevn/', cn: '十一' },
          { en: 'twelve', phonetic: '/twelv/', cn: '十二' },
          { en: 'thirteen', phonetic: '/ˌθɜːˈtiːn/', cn: '十三' },
          { en: 'fourteen', phonetic: '/ˌfɔːˈtiːn/', cn: '十四' },
          { en: 'fifteen', phonetic: '/ˌfɪfˈtiːn/', cn: '十五' },
          { en: 'twenty', phonetic: '/ˈtwenti/', cn: '二十' }
        ],
        sentences: [
          { en: 'How many kites do you see?', cn: '你看见多少只风筝？' },
          { en: 'I see 12!', cn: '我看见12只！' },
          { en: 'How many crayons do you have?', cn: '你有多少支蜡笔？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'How many birds do you see?', cn: '你看见多少只鸟？' },
          { speaker: 'B', avatar: 'b', en: 'I see 15!', cn: '我看见15只！' }
        ]
      }
    ],
    g4_v1: [
      {
        id: 'u1', name: 'Unit 1 My classroom', emoji: '🏫',
        words: [
          { en: 'classroom', phonetic: '/ˈklɑːsruːm/', cn: '教室' },
          { en: 'window', phonetic: '/ˈwɪndəʊ/', cn: '窗户' },
          { en: 'door', phonetic: '/dɔː(r)/', cn: '门' },
          { en: 'picture', phonetic: '/ˈpɪktʃə(r)/', cn: '图画' },
          { en: 'light', phonetic: '/laɪt/', cn: '灯' },
          { en: 'blackboard', phonetic: '/ˈblækbɔːd/', cn: '黑板' }
        ],
        sentences: [
          { en: 'What\'s in the classroom?', cn: '教室里有什么？' },
          { en: 'Let\'s clean the classroom.', cn: '让我们打扫教室吧。' },
          { en: 'Open the door, please.', cn: '请开门。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Where is the picture?', cn: '图画在哪里？' },
          { speaker: 'B', avatar: 'b', en: 'It\'s near the window.', cn: '它在窗户旁边。' }
        ]
      },
      {
        id: 'u2', name: 'Unit 2 My schoolbag', emoji: '🎒',
        words: [
          { en: 'schoolbag', phonetic: '/ˈskuːlbæɡ/', cn: '书包' },
          { en: 'maths book', phonetic: '/mæθs bʊk/', cn: '数学书' },
          { en: 'English book', phonetic: '/ˈɪŋɡlɪʃ bʊk/', cn: '英语书' },
          { en: 'Chinese book', phonetic: '/tʃaɪˈniːz bʊk/', cn: '语文书' },
          { en: 'storybook', phonetic: '/ˈstɔːribʊk/', cn: '故事书' },
          { en: 'notebook', phonetic: '/ˈnəʊtbʊk/', cn: '笔记本' }
        ],
        sentences: [
          { en: 'What\'s in your schoolbag?', cn: '你的书包里有什么？' },
          { en: 'An English book and a maths book.', cn: '一本英语书和一本数学书。' },
          { en: 'I lost my schoolbag.', cn: '我的书包丢了。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'What colour is it?', cn: '它是什么颜色的？' },
          { speaker: 'B', avatar: 'b', en: 'It\'s blue and white.', cn: '它是蓝白相间的。' }
        ]
      },
      {
        id: 'u3', name: 'Unit 3 My friends', emoji: '👫',
        words: [
          { en: 'tall', phonetic: '/tɔːl/', cn: '高的' },
          { en: 'strong', phonetic: '/strɒŋ/', cn: '强壮的' },
          { en: 'friendly', phonetic: '/ˈfrendli/', cn: '友好的' },
          { en: 'quiet', phonetic: '/ˈkwaɪət/', cn: '安静的' },
          { en: 'hair', phonetic: '/heə(r)/', cn: '头发' },
          { en: 'shoe', phonetic: '/ʃuː/', cn: '鞋子' }
        ],
        sentences: [
          { en: 'I have a good friend.', cn: '我有一个好朋友。' },
          { en: 'He\'s tall and strong.', cn: '他又高又壮。' },
          { en: 'She has long hair.', cn: '她有一头长发。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Who is he?', cn: '他是谁？' },
          { speaker: 'B', avatar: 'b', en: 'He\'s Zhang Peng.', cn: '他是张鹏。' }
        ]
      },
      {
        id: 'u4', name: 'Unit 4 My home', emoji: '🏠',
        words: [
          { en: 'bedroom', phonetic: '/ˈbedruːm/', cn: '卧室' },
          { en: 'living room', phonetic: '/ˈlɪvɪŋ ruːm/', cn: '客厅' },
          { en: 'kitchen', phonetic: '/ˈkɪtʃɪn/', cn: '厨房' },
          { en: 'bathroom', phonetic: '/ˈbɑːθruːm/', cn: '浴室' },
          { en: 'bed', phonetic: '/bed/', cn: '床' },
          { en: 'phone', phonetic: '/fəʊn/', cn: '电话' }
        ],
        sentences: [
          { en: 'Where is the cat?', cn: '猫在哪里？' },
          { en: 'Is she in the living room?', cn: '她在客厅吗？' },
          { en: 'No, she isn\'t.', cn: '不，她不在。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Is it in your hand?', cn: '它在你的手里吗？' },
          { speaker: 'B', avatar: 'b', en: 'Yes, it is!', cn: '是的，它在！' }
        ]
      },
      {
        id: 'u5', name: 'Unit 5 Dinner\'s ready', emoji: '🍽️',
        words: [
          { en: 'beef', phonetic: '/biːf/', cn: '牛肉' },
          { en: 'chicken', phonetic: '/ˈtʃɪkɪn/', cn: '鸡肉' },
          { en: 'noodles', phonetic: '/ˈnuːdlz/', cn: '面条' },
          { en: 'soup', phonetic: '/suːp/', cn: '汤' },
          { en: 'vegetable', phonetic: '/ˈvedʒtəbl/', cn: '蔬菜' },
          { en: 'chopsticks', phonetic: '/ˈtʃɒpstɪks/', cn: '筷子' }
        ],
        sentences: [
          { en: 'What would you like for dinner?', cn: '你晚餐想吃什么？' },
          { en: 'I\'d like some beef and noodles.', cn: '我想要一些牛肉和面条。' },
          { en: 'Dinner\'s ready!', cn: '晚餐准备好了！' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Would you like a knife and fork?', cn: '你想要刀叉吗？' },
          { speaker: 'B', avatar: 'b', en: 'No, thanks. I can use chopsticks.', cn: '不，谢谢。我会用筷子。' }
        ]
      },
      {
        id: 'u6', name: 'Unit 6 Meet my family!', emoji: '👪',
        words: [
          { en: 'family', phonetic: '/ˈfæməli/', cn: '家庭' },
          { en: 'parents', phonetic: '/ˈpeərənts/', cn: '父母' },
          { en: 'uncle', phonetic: '/ˈʌŋkl/', cn: '叔叔' },
          { en: 'aunt', phonetic: '/ɑːnt/', cn: '阿姨' },
          { en: 'cousin', phonetic: '/ˈkʌzn/', cn: '表亲' },
          { en: 'baby', phonetic: '/ˈbeɪbi/', cn: '婴儿' }
        ],
        sentences: [
          { en: 'How many people are there in your family?', cn: '你家有几口人？' },
          { en: 'Three.', cn: '三口人。' },
          { en: 'My family has six people.', cn: '我家有六口人。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Is this your uncle?', cn: '这是你的叔叔吗？' },
          { speaker: 'B', avatar: 'b', en: 'Yes, it is. He\'s a football player.', cn: '是的，他是一名足球运动员。' }
        ]
      }
    ],
    g4_v2: [
      {
        id: 'u1', name: 'Unit 1 My school', emoji: '🏫',
        words: [
          { en: 'first floor', phonetic: '/fɜːst flɔː(r)/', cn: '一楼' },
          { en: 'second floor', phonetic: '/ˈsekənd flɔː(r)/', cn: '二楼' },
          { en: 'teachers\' office', phonetic: '/ˈtiːtʃəz ˈɒfɪs/', cn: '教师办公室' },
          { en: 'library', phonetic: '/ˈlaɪbrəri/', cn: '图书馆' },
          { en: 'playground', phonetic: '/ˈpleɪɡraʊnd/', cn: '操场' },
          { en: 'computer room', phonetic: '/kəmˈpjuːtə(r) ruːm/', cn: '计算机房' }
        ],
        sentences: [
          { en: 'Where\'s the teachers\' office?', cn: '教师办公室在哪里？' },
          { en: 'It\'s on the second floor.', cn: '它在二楼。' },
          { en: 'Is this the teachers\' office?', cn: '这是教师办公室吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Excuse me, where\'s the library?', cn: '打扰一下，图书馆在哪里？' },
          { speaker: 'B', avatar: 'b', en: 'It\'s on the first floor.', cn: '它在一楼。' }
        ]
      },
      {
        id: 'u2', name: 'Unit 2 What time is it?', emoji: '⏰',
        words: [
          { en: 'breakfast', phonetic: '/ˈbrekfəst/', cn: '早餐' },
          { en: 'lunch', phonetic: '/lʌntʃ/', cn: '午餐' },
          { en: 'dinner', phonetic: '/ˈdɪnə(r)/', cn: '晚餐' },
          { en: 'class', phonetic: '/klɑːs/', cn: '课' },
          { en: 'music', phonetic: '/ˈmjuːzɪk/', cn: '音乐' },
          { en: 'PE', phonetic: '/ˌpiː ˈiː/', cn: '体育' }
        ],
        sentences: [
          { en: 'What time is it?', cn: '现在几点了？' },
          { en: 'It\'s 6 o\'clock.', cn: '现在6点了。' },
          { en: 'It\'s time for dinner.', cn: '该吃晚餐了。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'What time is it?', cn: '现在几点了？' },
          { speaker: 'B', avatar: 'b', en: 'It\'s time to go home.', cn: '该回家了。' }
        ]
      },
      {
        id: 'u3', name: 'Unit 3 Weather', emoji: '🌤️',
        words: [
          { en: 'cold', phonetic: '/kəʊld/', cn: '冷的' },
          { en: 'cool', phonetic: '/kuːl/', cn: '凉爽的' },
          { en: 'warm', phonetic: '/wɔːm/', cn: '温暖的' },
          { en: 'hot', phonetic: '/hɒt/', cn: '热的' },
          { en: 'sunny', phonetic: '/ˈsʌni/', cn: '晴朗的' },
          { en: 'windy', phonetic: '/ˈwɪndi/', cn: '有风的' }
        ],
        sentences: [
          { en: 'What\'s the weather like?', cn: '天气怎么样？' },
          { en: 'It\'s cold outside.', cn: '外面很冷。' },
          { en: 'Can I go outside?', cn: '我能出去吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Is it cold?', cn: '冷吗？' },
          { speaker: 'B', avatar: 'b', en: 'No, it\'s warm today.', cn: '不，今天很暖和。' }
        ]
      },
      {
        id: 'u4', name: 'Unit 4 At the farm', emoji: '🚜',
        words: [
          { en: 'tomato', phonetic: '/təˈmɑːtəʊ/', cn: '西红柿' },
          { en: 'potato', phonetic: '/pəˈteɪtəʊ/', cn: '土豆' },
          { en: 'green beans', phonetic: '/ɡriːn biːnz/', cn: '豆角' },
          { en: 'carrot', phonetic: '/ˈkærət/', cn: '胡萝卜' },
          { en: 'horse', phonetic: '/hɔːs/', cn: '马' },
          { en: 'cow', phonetic: '/kaʊ/', cn: '奶牛' }
        ],
        sentences: [
          { en: 'What are these?', cn: '这些是什么？' },
          { en: 'They\'re tomatoes.', cn: '它们是西红柿。' },
          { en: 'Are these carrots?', cn: '这些是胡萝卜吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Are those sheep?', cn: '那些是绵羊吗？' },
          { speaker: 'B', avatar: 'b', en: 'No, they\'re goats.', cn: '不，它们是山羊。' }
        ]
      },
      {
        id: 'u5', name: 'Unit 5 My clothes', emoji: '👗',
        words: [
          { en: 'clothes', phonetic: '/kləʊðz/', cn: '衣服' },
          { en: 'pants', phonetic: '/pænts/', cn: '裤子' },
          { en: 'hat', phonetic: '/hæt/', cn: '帽子' },
          { en: 'dress', phonetic: '/dres/', cn: '连衣裙' },
          { en: 'skirt', phonetic: '/skɜːt/', cn: '半身裙' },
          { en: 'coat', phonetic: '/kəʊt/', cn: '外套' }
        ],
        sentences: [
          { en: 'Are these yours?', cn: '这些是你的吗？' },
          { en: 'No, they aren\'t.', cn: '不，它们不是。' },
          { en: 'Whose coat is this?', cn: '这是谁的外套？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Is this your skirt?', cn: '这是你的裙子吗？' },
          { speaker: 'B', avatar: 'b', en: 'Yes, it is. Thank you!', cn: '是的，谢谢你！' }
        ]
      },
      {
        id: 'u6', name: 'Unit 6 Shopping', emoji: '🛍️',
        words: [
          { en: 'gloves', phonetic: '/ɡlʌvz/', cn: '手套' },
          { en: 'scarf', phonetic: '/skɑːf/', cn: '围巾' },
          { en: 'umbrella', phonetic: '/ʌmˈbrelə/', cn: '雨伞' },
          { en: 'sunglasses', phonetic: '/ˈsʌnɡlɑːsɪz/', cn: '太阳镜' },
          { en: 'pretty', phonetic: '/ˈprɪti/', cn: '漂亮的' },
          { en: 'expensive', phonetic: '/ɪkˈspensɪv/', cn: '昂贵的' }
        ],
        sentences: [
          { en: 'Can I help you?', cn: '我能为您效劳吗？' },
          { en: 'How much is it?', cn: '它多少钱？' },
          { en: 'It\'s too expensive.', cn: '它太贵了。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Can I try this dress on?', cn: '我能试试这条裙子吗？' },
          { speaker: 'B', avatar: 'b', en: 'Of course! Size 6, please.', cn: '当然！请拿6号的。' }
        ]
      }
    ],
    g5_v1: [
      {
        id: 'u1', name: 'Unit 1 What\'s he like?', emoji: '👨‍🏫',
        words: [
          { en: 'old', phonetic: '/əʊld/', cn: '年老的' },
          { en: 'young', phonetic: '/jʌŋ/', cn: '年轻的' },
          { en: 'funny', phonetic: '/ˈfʌni/', cn: '滑稽的' },
          { en: 'kind', phonetic: '/kaɪnd/', cn: '和蔼的' },
          { en: 'strict', phonetic: '/strɪkt/', cn: '严格的' },
          { en: 'polite', phonetic: '/pəˈlaɪt/', cn: '有礼貌的' }
        ],
        sentences: [
          { en: 'Who\'s your art teacher?', cn: '谁是你的美术老师？' },
          { en: 'Mr Jones.', cn: '琼斯先生。' },
          { en: 'Is he young?', cn: '他年轻吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Is she strict?', cn: '她严格吗？' },
          { speaker: 'B', avatar: 'b', en: 'Yes, but she\'s very kind.', cn: '是的，但她很和蔼。' }
        ]
      },
      {
        id: 'u2', name: 'Unit 2 My week', emoji: '📅',
        words: [
          { en: 'Monday', phonetic: '/ˈmʌndeɪ/', cn: '星期一' },
          { en: 'Tuesday', phonetic: '/ˈtjuːzdeɪ/', cn: '星期二' },
          { en: 'Wednesday', phonetic: '/ˈwenzdeɪ/', cn: '星期三' },
          { en: 'Thursday', phonetic: '/ˈθɜːzdeɪ/', cn: '星期四' },
          { en: 'Friday', phonetic: '/ˈfraɪdeɪ/', cn: '星期五' },
          { en: 'weekend', phonetic: '/ˌwiːkˈend/', cn: '周末' }
        ],
        sentences: [
          { en: 'What do you have on Thursdays?', cn: '星期四你有什么课？' },
          { en: 'I have maths, English and music.', cn: '我有数学、英语和音乐。' },
          { en: 'Do you often read books?', cn: '你经常看书吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'What do you do on the weekend?', cn: '你周末做什么？' },
          { speaker: 'B', avatar: 'b', en: 'I often play football.', cn: '我经常踢足球。' }
        ]
      },
      {
        id: 'u3', name: 'Unit 3 What would you like?', emoji: '🍱',
        words: [
          { en: 'sandwich', phonetic: '/ˈsænwɪtʃ/', cn: '三明治' },
          { en: 'salad', phonetic: '/ˈsæləd/', cn: '沙拉' },
          { en: 'hamburger', phonetic: '/ˈhæmbɜːɡə(r)/', cn: '汉堡包' },
          { en: 'ice cream', phonetic: '/ˌaɪs ˈkriːm/', cn: '冰淇淋' },
          { en: 'tea', phonetic: '/tiː/', cn: '茶' },
          { en: 'fresh', phonetic: '/freʃ/', cn: '新鲜的' }
        ],
        sentences: [
          { en: 'What would you like to eat?', cn: '你想吃什么？' },
          { en: 'A sandwich, please.', cn: '请给我一个三明治。' },
          { en: 'What\'s your favourite food?', cn: '你最喜欢的食物是什么？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'I\'d like some noodles.', cn: '我想要一些面条。' },
          { speaker: 'B', avatar: 'b', en: 'They\'re delicious!', cn: '它们很美味！' }
        ]
      },
      {
        id: 'u4', name: 'Unit 4 What can you do?', emoji: '🎭',
        words: [
          { en: 'sing', phonetic: '/sɪŋ/', cn: '唱歌' },
          { en: 'dance', phonetic: '/dɑːns/', cn: '跳舞' },
          { en: 'draw cartoons', phonetic: '/drɔː kɑːˈtuːnz/', cn: '画漫画' },
          { en: 'cook', phonetic: '/kʊk/', cn: '烹饪' },
          { en: 'swim', phonetic: '/swɪm/', cn: '游泳' },
          { en: 'play ping-pong', phonetic: '/pleɪ ˈpɪŋ pɒŋ/', cn: '打乒乓球' }
        ],
        sentences: [
          { en: 'What can you do?', cn: '你会做什么？' },
          { en: 'I can sing English songs.', cn: '我会唱英文歌。' },
          { en: 'Can you cook?', cn: '你会做饭吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Can you do any kung fu?', cn: '你会功夫吗？' },
          { speaker: 'B', avatar: 'b', en: 'Yes, I can.', cn: '是的，我会。' }
        ]
      },
      {
        id: 'u5', name: 'Unit 5 There is a big bed', emoji: '🛏️',
        words: [
          { en: 'clock', phonetic: '/klɒk/', cn: '时钟' },
          { en: 'plant', phonetic: '/plɑːnt/', cn: '植物' },
          { en: 'bottle', phonetic: '/ˈbɒtl/', cn: '瓶子' },
          { en: 'bike', phonetic: '/baɪk/', cn: '自行车' },
          { en: 'photo', phonetic: '/ˈfəʊtəʊ/', cn: '照片' },
          { en: 'front', phonetic: '/frʌnt/', cn: '前面' }
        ],
        sentences: [
          { en: 'There is a big bed.', cn: '有一张大床。' },
          { en: 'There are so many plants.', cn: '有很多植物。' },
          { en: 'My computer is on the desk.', cn: '我的电脑在书桌上。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Your room is really nice!', cn: '你的房间真漂亮！' },
          { speaker: 'B', avatar: 'b', en: 'There is a big bed.', cn: '有一张大床。' }
        ]
      },
      {
        id: 'u6', name: 'Unit 6 In a nature park', emoji: '🏞️',
        words: [
          { en: 'forest', phonetic: '/ˈfɒrɪst/', cn: '森林' },
          { en: 'river', phonetic: '/ˈrɪvə(r)/', cn: '河流' },
          { en: 'lake', phonetic: '/leɪk/', cn: '湖泊' },
          { en: 'mountain', phonetic: '/ˈmaʊntɪn/', cn: '高山' },
          { en: 'hill', phonetic: '/hɪl/', cn: '小山' },
          { en: 'tree', phonetic: '/triː/', cn: '树' }
        ],
        sentences: [
          { en: 'Is there a river in the park?', cn: '公园里有河流吗？' },
          { en: 'Yes, there is.', cn: '是的，有。' },
          { en: 'Are there any tall buildings?', cn: '有高楼吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'The nature park is so quiet!', cn: '自然公园真安静！' },
          { speaker: 'B', avatar: 'b', en: 'There is a small village.', cn: '有一个小村庄。' }
        ]
      }
    ],
    g5_v2: [
      {
        id: 'u1', name: 'Unit 1 My day', emoji: '☀️',
        words: [
          { en: 'eat breakfast', phonetic: '/iːt ˈbrekfəst/', cn: '吃早餐' },
          { en: 'do morning exercises', phonetic: '/duː ˈmɔːnɪŋ ˈeksəsaɪzɪz/', cn: '做早操' },
          { en: 'have class', phonetic: '/hæv klɑːs/', cn: '上课' },
          { en: 'eat lunch', phonetic: '/iːt lʌntʃ/', cn: '吃午餐' },
          { en: 'play sports', phonetic: '/pleɪ ˈspɔːts/', cn: '进行体育运动' },
          { en: 'go for a walk', phonetic: '/ɡəʊ fɔː(r) ə wɔːk/', cn: '散步' }
        ],
        sentences: [
          { en: 'When do you get up?', cn: '你什么时候起床？' },
          { en: 'I usually get up at 7 o\'clock.', cn: '我通常7点起床。' },
          { en: 'What do you do on the weekend?', cn: '你周末做什么？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Why are you shopping today?', cn: '你今天为什么购物？' },
          { speaker: 'B', avatar: 'b', en: 'My mother is busy.', cn: '我的妈妈很忙。' }
        ]
      },
      {
        id: 'u2', name: 'Unit 2 My favourite season', emoji: '🍂',
        words: [
          { en: 'spring', phonetic: '/sprɪŋ/', cn: '春天' },
          { en: 'summer', phonetic: '/ˈsʌmə(r)/', cn: '夏天' },
          { en: 'autumn', phonetic: '/ˈɔːtəm/', cn: '秋天' },
          { en: 'winter', phonetic: '/ˈwɪntə(r)//', cn: '冬天' },
          { en: 'season', phonetic: '/ˈsiːzn/', cn: '季节' },
          { en: 'picnic', phonetic: '/ˈpɪknɪk/', cn: '野餐' }
        ],
        sentences: [
          { en: 'Which season do you like best?', cn: '你最喜欢哪个季节？' },
          { en: 'I like spring best.', cn: '我最喜欢春天。' },
          { en: 'Why?', cn: '为什么？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'I like winter best.', cn: '我最喜欢冬天。' },
          { speaker: 'B', avatar: 'b', en: 'Because I can play in the snow!', cn: '因为我可以在雪地里玩！' }
        ]
      },
      {
        id: 'u3', name: 'Unit 3 My school calendar', emoji: '📆',
        words: [
          { en: 'January', phonetic: '/ˈdʒænjuəri/', cn: '一月' },
          { en: 'February', phonetic: '/ˈfebruəri/', cn: '二月' },
          { en: 'March', phonetic: '/mɑːtʃ/', cn: '三月' },
          { en: 'April', phonetic: '/ˈeɪprəl/', cn: '四月' },
          { en: 'May', phonetic: '/meɪ/', cn: '五月' },
          { en: 'June', phonetic: '/dʒuːn/', cn: '六月' }
        ],
        sentences: [
          { en: 'When is the sports meet?', cn: '运动会在什么时候？' },
          { en: 'It\'s in April.', cn: '在四月。' },
          { en: 'We\'ll have an Easter party.', cn: '我们将有一个复活节派对。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'When is your birthday?', cn: '你的生日是什么时候？' },
          { speaker: 'B', avatar: 'b', en: 'My birthday is in May.', cn: '我的生日在五月。' }
        ]
      },
      {
        id: 'u4', name: 'Unit 4 When is the art show?', emoji: '🎨',
        words: [
          { en: 'first', phonetic: '/fɜːst/', cn: '第一' },
          { en: 'second', phonetic: '/ˈsekənd/', cn: '第二' },
          { en: 'third', phonetic: '/θɜːd/', cn: '第三' },
          { en: 'fourth', phonetic: '/fɔːθ/', cn: '第四' },
          { en: 'fifth', phonetic: '/fɪfθ/', cn: '第五' },
          { en: 'special', phonetic: '/ˈspeʃl/', cn: '特别的' }
        ],
        sentences: [
          { en: 'When is the art show?', cn: '艺术展是什么时候？' },
          { en: 'It\'s on May 1st.', cn: '它在5月1日。' },
          { en: 'April Fool\'s Day is on April 1st.', cn: '愚人节在4月1日。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'When is your birthday?', cn: '你的生日是什么时候？' },
          { speaker: 'B', avatar: 'b', en: 'It\'s on November 30th.', cn: '它在11月30日。' }
        ]
      },
      {
        id: 'u5', name: 'Unit 5 Whose dog is it?', emoji: '🐕',
        words: [
          { en: 'mine', phonetic: '/maɪn/', cn: '我的' },
          { en: 'yours', phonetic: '/jɔːz/', cn: '你的' },
          { en: 'his', phonetic: '/hɪz/', cn: '他的' },
          { en: 'hers', phonetic: '/hɜːz/', cn: '她的' },
          { en: 'theirs', phonetic: '/ðeəz/', cn: '他们的' },
          { en: 'climbing', phonetic: '/ˈklaɪmɪŋ/', cn: '攀爬' }
        ],
        sentences: [
          { en: 'Whose dog is it?', cn: '它是谁的狗？' },
          { en: 'It\'s mine.', cn: '它是我的。' },
          { en: 'The dog is climbing.', cn: '狗正在攀爬。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Is he drinking water?', cn: '他正在喝水吗？' },
          { speaker: 'B', avatar: 'b', en: 'No, he isn\'t. He\'s eating.', cn: '不，他没有。他正在吃东西。' }
        ]
      },
      {
        id: 'u6', name: 'Unit 6 Work quietly!', emoji: '🤫',
        words: [
          { en: 'doing morning exercises', phonetic: '/ˈduːɪŋ ˈmɔːnɪŋ ˈeksəsaɪzɪz/', cn: '做早操' },
          { en: 'having class', phonetic: '/ˈhævɪŋ klɑːs/', cn: '上课' },
          { en: 'eating lunch', phonetic: '/ˈiːtɪŋ lʌntʃ/', cn: '吃午餐' },
          { en: 'reading a book', phonetic: '/ˈriːdɪŋ ə bʊk/', cn: '看书' },
          { en: 'listening to music', phonetic: '/ˈlɪsnɪŋ tə ˈmjuːzɪk/', cn: '听音乐' },
          { en: 'keep', phonetic: '/kiːp/', cn: '保持' }
        ],
        sentences: [
          { en: 'What are you doing?', cn: '你正在做什么？' },
          { en: 'I\'m reading a book.', cn: '我正在看书。' },
          { en: 'Keep your desk clean.', cn: '保持你的书桌干净。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Shh! Talk quietly.', cn: '嘘！小声说话。' },
          { speaker: 'B', avatar: 'b', en: 'OK. I\'m sorry.', cn: '好的，对不起。' }
        ]
      }
    ],
    g6_v1: [
      {
        id: 'u1', name: 'Unit 1 How can I get there?', emoji: '🗺️',
        words: [
          { en: 'science museum', phonetic: '/ˈsaɪəns mjuˈziːəm/', cn: '科学博物馆' },
          { en: 'hospital', phonetic: '/ˈhɒspɪtl/', cn: '医院' },
          { en: 'cinema', phonetic: '/ˈsɪnəmə/', cn: '电影院' },
          { en: 'bookstore', phonetic: '/ˈbʊkstɔː(r)/', cn: '书店' },
          { en: 'crossing', phonetic: '/ˈkrɒsɪŋ/', cn: '十字路口' },
          { en: 'turn', phonetic: '/tɜːn/', cn: '转弯' }
        ],
        sentences: [
          { en: 'Where is the museum shop?', cn: '博物馆商店在哪里？' },
          { en: 'It\'s near the door.', cn: '它在门附近。' },
          { en: 'How can I get there?', cn: '我怎么到那里？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Is it far?', cn: '它远吗？' },
          { speaker: 'B', avatar: 'b', en: 'No, turn left at the cinema.', cn: '不远，在电影院左转。' }
        ]
      },
      {
        id: 'u2', name: 'Unit 2 Ways to go to school', emoji: '🚌',
        words: [
          { en: 'on foot', phonetic: '/ɒn fʊt/', cn: '步行' },
          { en: 'by bus', phonetic: '/baɪ bʌs/', cn: '乘公交车' },
          { en: 'by plane', phonetic: '/baɪ pleɪn/', cn: '乘飞机' },
          { en: 'by taxi', phonetic: '/baɪ ˈtæksi/', cn: '乘出租车' },
          { en: 'by ship', phonetic: '/baɪ ʃɪp/', cn: '乘船' },
          { en: 'by subway', phonetic: '/baɪ ˈsʌbweɪ/', cn: '乘地铁' }
        ],
        sentences: [
          { en: 'How do you come to school?', cn: '你怎么来学校？' },
          { en: 'Usually, I come on foot.', cn: '通常，我步行来。' },
          { en: 'Don\'t go at the red light!', cn: '红灯时不要走！' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'How does Mrs Miller go to work?', cn: '米勒夫人怎么去上班？' },
          { speaker: 'B', avatar: 'b', en: 'She goes by subway.', cn: '她乘地铁去。' }
        ]
      },
      {
        id: 'u3', name: 'Unit 3 My weekend plan', emoji: '🎬',
        words: [
          { en: 'visit', phonetic: '/ˈvɪzɪt/', cn: '拜访' },
          { en: 'film', phonetic: '/fɪlm/', cn: '电影' },
          { en: 'trip', phonetic: '/trɪp/', cn: '旅行' },
          { en: 'supermarket', phonetic: '/ˈsuːpəmɑːkɪt/', cn: '超市' },
          { en: 'tonight', phonetic: '/təˈnaɪt/', cn: '今晚' },
          { en: 'tomorrow', phonetic: '/təˈmɒrəʊ/', cn: '明天' }
        ],
        sentences: [
          { en: 'What are you going to do tomorrow?', cn: '你明天打算做什么？' },
          { en: 'I\'m going to take a trip.', cn: '我打算去旅行。' },
          { en: 'Where are you going?', cn: '你打算去哪里？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Are you going to the cinema?', cn: '你打算去电影院吗？' },
          { speaker: 'B', avatar: 'b', en: 'Yes, we\'re going to see a film.', cn: '是的，我们打算去看电影。' }
        ]
      },
      {
        id: 'u4', name: 'Unit 4 I have a pen pal', emoji: '✉️',
        words: [
          { en: 'hobbies', phonetic: '/ˈhɒbiz/', cn: '爱好' },
          { en: 'reading', phonetic: '/ˈriːdɪŋ/', cn: '阅读' },
          { en: 'dancing', phonetic: '/ˈdɑːnsɪŋ/', cn: '跳舞' },
          { en: 'singing', phonetic: '/ˈsɪŋɪŋ/', cn: '唱歌' },
          { en: 'doing kung fu', phonetic: '/ˈduːɪŋ kʌŋ fuː/', cn: '练功夫' },
          { en: 'cooking', phonetic: '/ˈkʊkɪŋ/', cn: '烹饪' }
        ],
        sentences: [
          { en: 'What are Peter\'s hobbies?', cn: '彼得的爱好是什么？' },
          { en: 'He likes reading stories.', cn: '他喜欢读故事。' },
          { en: 'Does he live in Sydney?', cn: '他住在悉尼吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'I have a new pen pal.', cn: '我有一个新笔友。' },
          { speaker: 'B', avatar: 'b', en: 'Really? What\'s his name?', cn: '真的吗？他叫什么名字？' }
        ]
      },
      {
        id: 'u5', name: 'Unit 5 What does he do?', emoji: '👨‍⚕️',
        words: [
          { en: 'factory worker', phonetic: '/ˈfæktəri ˈwɜːkə(r)/', cn: '工厂工人' },
          { en: 'postman', phonetic: '/ˈpəʊstmən/', cn: '邮递员' },
          { en: 'businessman', phonetic: '/ˈbɪznəsmæn/', cn: '商人' },
          { en: 'police officer', phonetic: '/pəˈliːs ˈɒfɪsə(r)/', cn: '警察' },
          { en: 'fisherman', phonetic: '/ˈfɪʃəmən/', cn: '渔民' },
          { en: 'scientist', phonetic: '/ˈsaɪəntɪst/', cn: '科学家' }
        ],
        sentences: [
          { en: 'What does your father do?', cn: '你的父亲是做什么的？' },
          { en: 'He\'s a fisherman.', cn: '他是一名渔民。' },
          { en: 'Where does he work?', cn: '他在哪里工作？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'What does she do?', cn: '她是做什么的？' },
          { speaker: 'B', avatar: 'b', en: 'She\'s a head teacher.', cn: '她是一名校长。' }
        ]
      },
      {
        id: 'u6', name: 'Unit 6 How do you feel?', emoji: '😊',
        words: [
          { en: 'angry', phonetic: '/ˈæŋɡri/', cn: '生气的' },
          { en: 'afraid', phonetic: '/əˈfreɪd/', cn: '害怕的' },
          { en: 'sad', phonetic: '/sæd/', cn: '难过的' },
          { en: 'worried', phonetic: '/ˈwʌrid/', cn: '担心的' },
          { en: 'happy', phonetic: '/ˈhæpi/', cn: '快乐的' },
          { en: 'ill', phonetic: '/ɪl/', cn: '生病的' }
        ],
        sentences: [
          { en: 'How do you feel?', cn: '你感觉怎么样？' },
          { en: 'I\'m happy.', cn: '我很开心。' },
          { en: 'Don\'t be sad.', cn: '别难过。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Sarah is angry.', cn: '萨拉很生气。' },
          { speaker: 'B', avatar: 'b', en: 'She should see a doctor.', cn: '她应该去看医生。' }
        ]
      }
    ],
    g6_v2: [
      {
        id: 'u1', name: 'Unit 1 How tall are you?', emoji: '📏',
        words: [
          { en: 'younger', phonetic: '/ˈjʌŋɡə(r)/', cn: '更年轻的' },
          { en: 'older', phonetic: '/ˈəʊldə(r)/', cn: '更年长的' },
          { en: 'taller', phonetic: '/ˈtɔːlə(r)/', cn: '更高的' },
          { en: 'shorter', phonetic: '/ˈʃɔːtə(r)/', cn: '更矮的' },
          { en: 'longer', phonetic: '/ˈlɒŋɡə(r)/', cn: '更长的' },
          { en: 'thinner', phonetic: '/ˈθɪnə(r)/', cn: '更瘦的' }
        ],
        sentences: [
          { en: 'How tall are you?', cn: '你有多高？' },
          { en: 'I\'m 1.65 metres.', cn: '我1.65米。' },
          { en: 'You\'re shorter than me.', cn: '你比我矮。' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'How heavy are you?', cn: '你有多重？' },
          { speaker: 'B', avatar: 'b', en: 'I\'m 48 kilograms.', cn: '我48公斤。' }
        ]
      },
      {
        id: 'u2', name: 'Unit 2 Last weekend', emoji: '📆',
        words: [
          { en: 'cleaned', phonetic: '/kliːnd/', cn: '打扫了' },
          { en: 'stayed', phonetic: '/steɪd/', cn: '停留了' },
          { en: 'washed', phonetic: '/wɒʃt/', cn: '洗了' },
          { en: 'watched', phonetic: '/wɒtʃt/', cn: '观看了' },
          { en: 'had', phonetic: '/hæd/', cn: '有了；吃了' },
          { en: 'slept', phonetic: '/slept/', cn: '睡了' }
        ],
        sentences: [
          { en: 'What did you do last weekend?', cn: '你上周末做了什么？' },
          { en: 'I stayed at home.', cn: '我待在家里。' },
          { en: 'Did you see a film?', cn: '你看电影了吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'How was your weekend?', cn: '你的周末怎么样？' },
          { speaker: 'B', avatar: 'b', en: 'It was good, thank you.', cn: '很好，谢谢。' }
        ]
      },
      {
        id: 'u3', name: 'Unit 3 Where did you go?', emoji: '✈️',
        words: [
          { en: 'went', phonetic: '/went/', cn: '去了' },
          { en: 'camp', phonetic: '/kæmp/', cn: '露营' },
          { en: 'rode', phonetic: '/rəʊd/', cn: '骑了' },
          { en: 'hurt', phonetic: '/hɜːt/', cn: '受伤' },
          { en: 'ate', phonetic: '/eɪt/', cn: '吃了' },
          { en: 'took', phonetic: '/tʊk/', cn: '拍了；拿了' }
        ],
        sentences: [
          { en: 'Where did you go over the winter holiday?', cn: '寒假你去了哪里？' },
          { en: 'I went to Sanya.', cn: '我去了三亚。' },
          { en: 'How did you go there?', cn: '你怎么去的？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Did you go swimming?', cn: '你去游泳了吗？' },
          { speaker: 'B', avatar: 'b', en: 'Yes, I did. It was fun!', cn: '是的，很有趣！' }
        ]
      },
      {
        id: 'u4', name: 'Unit 4 Then and now', emoji: '🕰️',
        words: [
          { en: 'ago', phonetic: '/əˈɡəʊ/', cn: '以前' },
          { en: 'yesterday', phonetic: '/ˈjestədeɪ/', cn: '昨天' },
          { en: 'before', phonetic: '/bɪˈfɔː(r)/', cn: '以前' },
          { en: 'thin', phonetic: '/θɪn/', cn: '瘦的' },
          { en: 'heavy', phonetic: '/ˈhevi/', cn: '重的' },
          { en: 'active', phonetic: '/ˈæktɪv/', cn: '活跃的' }
        ],
        sentences: [
          { en: 'There was no gym in my school.', cn: '我的学校以前没有体育馆。' },
          { en: 'Now there\'s a new one.', cn: '现在有一个新的。' },
          { en: 'How do you know that?', cn: '你怎么知道的？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Tell us about your school, please.', cn: '请告诉我们关于你的学校。' },
          { speaker: 'B', avatar: 'b', en: 'There were no computers then.', cn: '那时没有电脑。' }
        ]
      },
      {
        id: 'u5', name: 'Unit 5 What are you doing?', emoji: '🎉',
        words: [
          { en: 'flying', phonetic: '/ˈflaɪɪŋ/', cn: '飞' },
          { en: 'jumping', phonetic: '/ˈdʒʌmpɪŋ/', cn: '跳' },
          { en: 'walking', phonetic: '/ˈwɔːkɪŋ/', cn: '走' },
          { en: 'swimming', phonetic: '/ˈswɪmɪŋ/', cn: '游泳' },
          { en: 'running', phonetic: '/ˈrʌnɪŋ/', cn: '跑' },
          { en: 'singing', phonetic: '/ˈsɪŋɪŋ/', cn: '唱歌' }
        ],
        sentences: [
          { en: 'What are you doing?', cn: '你正在做什么？' },
          { en: 'I\'m looking at the rabbits.', cn: '我正在看兔子。' },
          { en: 'Are they eating lunch?', cn: '它们正在吃午餐吗？' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'What is the elephant doing?', cn: '大象正在做什么？' },
          { speaker: 'B', avatar: 'b', en: 'It\'s drinking water.', cn: '它正在喝水。' }
        ]
      },
      {
        id: 'u6', name: 'Unit 6 My summer holiday', emoji: '🏖️',
        words: [
          { en: 'beach', phonetic: '/biːtʃ/', cn: '海滩' },
          { en: 'sea', phonetic: '/siː/', cn: '大海' },
          { en: 'travel', phonetic: '/ˈtrævl/', cn: '旅行' },
          { en: 'relax', phonetic: '/rɪˈlæks/', cn: '放松' },
          { en: 'enjoy', phonetic: '/ɪnˈdʒɔɪ/', cn: '享受' },
          { en: 'holiday', phonetic: '/ˈhɒlədeɪ/', cn: '假期' }
        ],
        sentences: [
          { en: 'What are you going to do this summer holiday?', cn: '这个暑假你打算做什么？' },
          { en: 'I\'m going to the beach.', cn: '我打算去海滩。' },
          { en: 'It will be fun!', cn: '那会很有趣！' }
        ],
        dialogues: [
          { speaker: 'A', avatar: 'a', en: 'Where will you go?', cn: '你将去哪里？' },
          { speaker: 'B', avatar: 'b', en: 'I\'ll visit my grandparents.', cn: '我将去看望我的祖父母。' }
        ]
      }
    ]
  }
};

<template>
    <div class="container">
        <h1>CalorieCam</h1>

        <div class="form-container">
            <div class="form-group">
                <label for="name">Имя блюда:</label>
                <input type="text" id="name" v-model="dishName" placeholder="Введите название блюда">
            </div>

            <div class="form-group">
                <label for="file">Загрузить изображение:</label>
                <input type="file" id="file" @change="handleFileUpload" accept="image/*">
                <div v-if="selectedFile" class="file-info">
                    Выбран файл: {{ selectedFile.name }}
                </div>
            </div>

            <button @click="submitForm" :disabled="!canSubmit" :class="{ 'loading': loading }">
                {{ loading ? 'Анализируем...' : 'Анализировать' }}
            </button>

            <div v-if="result" class="result">
                <h2>Результат анализа:</h2>
                <div>
                    <p><strong>Название блюда:</strong> {{ result.dish_name }}</p>
                    <p><strong>Калории:</strong> {{ result.calories }} ккал</p>
                    <p><strong>Белки:</strong> {{ result.protein }} г</p>
                    <p><strong>Жиры:</strong> {{ result.fat }} г</p>
                    <p><strong>Углеводы:</strong> {{ result.carbs }} г</p>
                </div>
            </div>

            <div v-if="error" class="error">
                <p>{{ error }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'App',
    data() {
        return {
            dishName: '',
            selectedFile: null,
            result: '',
            error: '',
            loading: false,
            apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8001'
            //apiUrl: import.meta.env.VITE_API_URL || 'http://caloriecam-dishes-service:8001'
        }
    },
    computed: {
        canSubmit() {
            return this.dishName.trim() !== '' && this.selectedFile !== null && !this.loading;
        }
    },
    methods: {
        handleFileUpload(event) {
            this.selectedFile = event.target.files[0];
            // Сбрасываем предыдущие результаты при выборе нового файла
            this.result = '';
            this.error = '';
        },
        async submitForm() {
            if (!this.canSubmit) return;

            this.loading = true;
            this.error = '';
            this.result = '';

            try {
                // Шаг 1: Загрузка изображения и получение предсказания
                const formData = new FormData();
                formData.append('file', this.selectedFile);

                console.log('Отправка запроса на загрузку изображения...');
                const uploadResponse = await axios.post(
                    `${this.apiUrl}/dish/load_image/${encodeURIComponent(this.dishName)}`,
                    formData,
                    {
                        headers: {
                            'Content-Type': 'multipart/form-data'
                        }
                    }
                );

                console.log('Ответ от сервера на загрузку:', uploadResponse.data);

                // Проверяем успешность загрузки и структуру ответа
                if (!uploadResponse.data) {
                    throw new Error('Пустой ответ от сервера');
                }

                if (uploadResponse.data.status !== 'success') {
                    throw new Error(`Ошибка при загрузке изображения: ${JSON.stringify(uploadResponse.data)}`);
                }

                // Получаем ID предсказания из URL
                // Предполагаем, что ID предсказания - это последний сегмент URL
                const urlParts = uploadResponse.config.url.split('/');
                const predictionName = decodeURIComponent(urlParts[urlParts.length - 1]);
                
                // Получаем список предсказаний и находим наше по имени
                const predictionsResponse = await axios.get(`${this.apiUrl}/dish/predict/${uploadResponse.data.id}`);
                
                console.log('Ответ от сервера с предсказанием:', predictionsResponse.data);

                // Отображаем результат
                if (predictionsResponse.data) {
                    this.result = predictionsResponse.data;
                } else {
                    this.result = `Анализ завершен, но результат не получен. Структура ответа: ${JSON.stringify(predictionsResponse.data)}`;
                }
            } catch (err) {
                console.error('Ошибка при отправке данных:', err);

                // Более детальное сообщение об ошибке
                if (err.response) {
                    // Ошибка от сервера
                    this.error = `Ошибка сервера: ${err.response.status} - ${JSON.stringify(err.response.data)}`;
                } else if (err.request) {
                    // Нет ответа от сервера
                    this.error = `Сервер не отвечает. URL запроса: ${err.config?.url}. Проверьте подключение или попробуйте позже.`;
                } else {
                    // Ошибка при настройке запроса
                    this.error = `Ошибка при анализе: ${err.message}`;
                }
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>

<style>
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
}

h1 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}

.form-container {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    font-weight: bold;
}

input[type="text"] {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

input[type="file"] {
    display: block;
    margin-top: 5px;
}

.file-info {
    margin-top: 8px;
    font-size: 14px;
    color: #666;
}

button {
    background-color: #4CAF50;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    width: 100%;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #45a049;
}

button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

button.loading {
    background-color: #8bc34a;
    cursor: wait;
}

.result {
    margin-top: 30px;
    padding: 15px;
    background-color: #e7f7e7;
    border-radius: 4px;
}

.error {
    margin-top: 20px;
    padding: 15px;
    background-color: #ffebee;
    color: #c62828;
    border-radius: 4px;
}
</style>
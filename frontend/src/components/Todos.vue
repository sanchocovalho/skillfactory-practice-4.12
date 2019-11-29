<template>
  <div class="container">
    <div class="col-sm-12">
      <h1 class="taskmanager">Менеджер задач</h1>
      <h5 class="text-left">Всего задач: {{ totalTasks }}</h5>
      <h5 class="text-left">Невыполненных: {{ uncompletedTasks }}</h5>
      <div class="d-flex flex-row justify-content-between">
        <div class="col-sm-3">
          <button type="button"
            id="task-add"
            class="btn btn-success btn-sm align-left d-block"
            v-b-modal.todo-modal>
            Добавить задачу
          </button>
        </div>
        <div class="col-sm-9">
          <confirmation
            :message="confirmationMessage"
            :alertvariant="confirmationAlertVariant"
            ref="confirmation">
          </confirmation>
        </div>
      </div>
      <table class="table table-dark table-stripped table-hover">
        <thead class="thead-light">
          <tr class="table-bordered">
            <th>ID</th>
            <th>Описание</th>
            <th>Статус</th>
            <th>Контроль</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(todo, index) in todos" :key="index"
            :class="{ 'bg-success': todo.is_completed }">
            <td class="todo-uid">{{ todo.uid }}</td>
            <td class="text-left">{{ todo.description }}</td>
            <td class="text-center">
              <span v-if="todo.is_completed">Выполнено</span>
              <span v-else>Не выполнено</span>
            </td>
            <td class="text-center">
              <div class="btn-group" role="group">
                <span v-if="todo.is_completed">
                <button
                  type="button"
                  class="btn btn-dark btn-sm"
                  @click="onUpdateSubmit(todo, false)">
                Сбросить
                </button>
                </span>
                <span v-else>
                <button
                  type="button"
                  class="btn btn-success btn-sm"
                  @click="onUpdateSubmit(todo, true)">
                Завершить
                </button>
                </span>
                &nbsp;
                <button type="button"
                  class="btn btn-danger btn-sm"
                  @click="deleteTodo(todo)">
                ×
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <b-modal
      ref="addTodoModal"
      id="todo-modal"
      centered
      title="Добавить задачу"
      hide-footer>
      <b-form
        @submit="onSubmit"
        @reset="onReset"
        class="w-100">
        <b-form-group
          id="form-description-group"
          label="Описание:"
          label-for="form-description-input">
          <b-form-input
            id="form-description-input"
            type="text"
            v-model="addTodoForm.description"
            required
            placeholder="Завести задачу">
          </b-form-input>
        </b-form-group>
        <b-form-group class="text-center">
        <button
          type="submit"
          class="btn btn-outline-success">
          Добавить
        </button>
        &nbsp;
        <button
          type="reset"
          class="btn btn-outline-danger">
          Сброс
        </button>
        </b-form-group>
      </b-form>
    </b-modal>

  </div>
</template>

<style>
button#task-add {
  margin-top: 20px;
  margin-bottom: 20px;
}
h1, td {
  text-align: left;
}
.taskmanager {
  margin-top: 20px;
  text-align: center;
  color: #2c3e50;
  font-weight: bold;
  font-size: 70px;
}
.todo-uid {
  text-align: center;
}
</style>

<script>
import axios from 'axios';
import Confirmation from './Confirmation.vue';

const dataURL = 'http://localhost:5000/';
// const dataURL = 'https://miniserver-skillfactory.herokuapp.com/';
const errorMsg = 'Ошибка сетевого соединения';
const successVariant = 'success';
const dangerVariant = 'danger';

export default {
  name: 'Todo',
  data() {
    return {
      todos: [],
      addTodoForm: {
        description: '',
      },
      totalTasks: '',
      uncompletedTasks: '',
      confirmationMessage: '',
      confirmationAlertVariant: '',
    };
  },
  methods: {
    getTodos() {
      axios.get(dataURL)
        .then((response) => {
          this.todos = response.data.tasks;
          this.totalTasks = `${response.data.total}`;
          this.uncompletedTasks = `${response.data.uncompleted}`;
        })
        .catch(() => {
          this.confirmationMessage = errorMsg;
          this.confirmationAlertVariant = dangerVariant;
          this.$refs.confirmation.showAlert(6);
        });
    },
    resetForm() {
      this.addTodoForm.description = '';
      this.addTodoForm.is_completed = [];
      this.updateTodoForm.description = '';
      this.updateTodoForm.is_completed = [];
    },
    onSubmit(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      const requestData = {
        description: this.addTodoForm.description,
        is_completed: false,
      };
      axios.post(dataURL, requestData)
        .then(() => {
          this.getTodos();
          this.confirmationMessage = `Задача "${requestData.description}" добавлена в список`;
          this.confirmationAlertVariant = successVariant;
        })
        .catch(() => {
          this.confirmationMessage = errorMsg;
          this.confirmationAlertVariant = dangerVariant;
        })
        .finally(() => {
          this.$refs.confirmation.showAlert(6);
        });
      this.resetForm();
    },
    onReset(event) {
      event.preventDefault();
      this.$refs.addTodoModal.hide();
      this.resetForm();
    },
    onUpdateSubmit(todo, status) {
      const requestData = {
        description: todo.description,
        is_completed: status,
      };
      const todoURL = dataURL + todo.uid;
      axios.put(todoURL, requestData)
        .then(() => {
          this.getTodos();
          this.confirmationMessage = 'Статус задачи изменен';
          this.confirmationAlertVariant = successVariant;
        })
        .catch(() => {
          this.confirmationMessage = errorMsg;
          this.confirmationAlertVariant = dangerVariant;
        })
        .finally(() => {
          this.$refs.confirmation.showAlert(6);
        });
    },
    deleteTodo(todo) {
      const todoURL = dataURL + todo.uid;
      axios.delete(todoURL)
        .then(() => {
          this.getTodos();
          this.confirmationMessage = 'Задача удалена из списка';
          this.confirmationAlertVariant = successVariant;
        })
        .catch(() => {
          this.confirmationMessage = errorMsg;
          this.confirmationAlertVariant = dangerVariant;
        })
        .finally(() => {
          this.$refs.confirmation.showAlert(6);
        });
    },
  },
  components: {
    confirmation: Confirmation,
  },
  created() {
    this.getTodos();
  },
};
</script>

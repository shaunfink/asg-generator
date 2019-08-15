<template>
  <div
      class="container">
    <div
        class="row">
      <div
          class="col-sm-10">
        <h1>
            ASG Generator
        </h1>

        <hr>

        <alert
            :message=message
            v-if="showMessage">
        </alert>

        <div
            class="btn-group"
            role="group">
          <button
              type="button"
              class="btn btn-success"
              v-b-modal.asg-modal>
            Add ASG
          </button>
          <button
              type="button"
              class="btn btn-success"
              v-b-modal.asg-upload-modal>
            Load JSON
          </button>
          <button
              type="button"
              class="btn btn-success"
              @click="generateAsg()">
            Generate JSON
          </button>
        </div>

        <br><br>

        <table
            class="table table-hover">
          <thead>
            <tr>
              <th
                  scope="col">
                Description</th>
              <th
                  scope="col">
                Destination</th>
              <th
                  scope="col">
                Log?</th>
              <th
                  scope="col">
                Ports</th>
              <th
                  scope="col">
                Protocol</th>
              <th
                  scope="col">
                Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
                v-for="(asg, index) in asgs"
                :key="index">
              <td>
                  {{ asg.description }}
              </td>
              <td>
                  {{ asg.destination }}
              </td>
              <td>
                  {{ asg.log }}
              </td>
              <td>
                  {{ asg.ports }}
              </td>
              <td>
                  {{ asg.protocol }}
              </td>
              <td>
                <div
                    class="btn-group"
                    role="group">
                  <button
                      type="button"
                      class="btn btn-warning btn-sm"
                      v-b-modal.asg-update-modal
                      @click="editAsg(asg)">
                    Update
                  </button>
                  <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="deleteAsg(asg)">
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>

    <b-modal
        ref="addAsgModal"
        id="asg-modal"
        title="Add a new ASG"
        hide-footer>

      <b-form
          @submit="onSubmitAdd"
          @reset="onResetAdd"
          class="w-100">

        <b-form-group
            id="form-description-group"
            label="Description:"
            label-for="form-description-input">
          <b-form-input
              id="form-description-input"
              type="text"
              v-model="addAsgForm.description"
              required
              placeholder="Enter ASG Description">
          </b-form-input>
        </b-form-group>

        <b-form-group
            id="form-destination-group"
            label="Destination:"
            label-for="form-destination-input">
          <b-form-input
              id="form-destination-input"
              type="text"
              v-model="addAsgForm.destination"
              required
              placeholder="Enter Destination (IP Address, IP Range or Network CIDR)">
          </b-form-input>
        </b-form-group>

        <b-form-group
            id="form-log-group">
          <b-form-checkbox-group
              v-model="addAsgForm.log"
              id="form-checks">
            <b-form-checkbox
                value="true">
              Log?
            </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>

        <b-form-group
            id="form-port-group"
            label="Ports:"
            label-for="form-port-input">
          <b-form-input
              id="form-port-input"
              type="text"
              v-model="addAsgForm.ports"
              required
              placeholder="Enter ASG Ports (Port or Port Range)">
          </b-form-input>
        </b-form-group>

        <b-form-group
            id="form-protocol-group"
            label="Protocol:"
            label-for="form-protocol-input">
          <b-form-group
              id="form-protocol-input">
            <b-form-radio
                v-model="addAsgForm.protocol"
                value="tcp">
              TCP
            </b-form-radio>
            <b-form-radio
                v-model="addAsgForm.protocol"
                value="udp">
              UDP
            </b-form-radio>
          </b-form-group>

        </b-form-group>

        <b-button-group>
          <b-button
              type="submit"
              variant="primary">
            Submit
          </b-button>
          <b-button
              type="reset"
              variant="danger">
            Reset
          </b-button>
        </b-button-group>

      </b-form>
    </b-modal>

    <b-modal
        ref="editASGModal"
        id="asg-update-modal"
        title="Update"
        hide-footer>
      <b-form
          @submit="onSubmitUpdate"
          @reset="onResetUpdate"
          class="w-100">
        <b-form-group
            id="form-description-edit-group"
            label="Description:"
            label-for="form-description-edit-input">
          <b-form-input
              id="form-description-edit-input"
              type="text"
              v-model="editAsgForm.description"
              required
              placeholder="Enter ASG Description">
          </b-form-input>
        </b-form-group>

        <b-form-group
            id="form-destination-edit-group"
            label="Destination:"
            label-for="form-destination-edit-input">
          <b-form-input
              id="form-destionation-edit-input"
              type="text"
              v-model="editAsgForm.destination"
              required
              placeholder="Enter Destination (IP Address, IP Range or Network CIDR)">
          </b-form-input>
        </b-form-group>

        <b-form-group
            id="form-log-edit-group">
          <b-form-checkbox-group
              v-model="editAsgForm.log"
              id="form-checks">
            <b-form-checkbox
                value="true">
              Log?
            </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>

        <b-form-group
            id="form-port-edit-group"
            label="Ports:"
            label-for="form-port-edit-input">
          <b-form-input
              id="form-port-edit-input"
              type="text"
              v-model="editAsgForm.ports"
              required
              placeholder="Enter ASG Ports (Port or Port Range)">
          </b-form-input>
        </b-form-group>

        <b-form-group
            id="form-protocol-edit-group"
            label="Protocol:"
            label-for="form-protocol-edit-input">
          <b-form-group
              id="form-protocol-edit-input">
            <b-form-radio
                v-model="editAsgForm.protocol"
                value="tcp">
              TCP
            </b-form-radio>
            <b-form-radio
                v-model="editAsgForm.protocol"
                value="udp">
              UDP
            </b-form-radio>
          </b-form-group>
        </b-form-group>

        <b-button-group>
          <b-button
              type="submit"
              variant="primary">
            Update
          </b-button>
          <b-button
              type="reset"
              variant="danger">
            Cancel
          </b-button>
        </b-button-group>

      </b-form>
    </b-modal>

    <b-modal
        ref="uploadASGModal"
        id="asg-upload-modal"
        title="Load ASG JSON"
        hide-footer>
      <b-form
          @submit="onSubmitJson"
          @reset="onResetJson"
          class="w-100">
        <b-form-group
            id="form-upload-group"
            label-for="form-upload-input">
          <b-form-file
              v-model="file"
              :state="Boolean(file)"
              placeholder="Choose a file or drop it here..."
              drop-placeholder="Drop file here..."
              id="file"
              ref="file"
              @change="handleFileUpload()"
              accept=".json">
          </b-form-file>
          <div class="mt-3">Selected file: {{ file ? file.name : '' }}</div>
        </b-form-group>

        <b-button-group>
          <b-button
              type="reset"
              variant="danger"
              class="btn btn-success">
            Clear
          </b-button>
          <b-button
              type="submit" variant="primary"
              class="btn btn-success">
            Submit
          </b-button>
        </b-button-group>

      </b-form>
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      asgs: [],
      addAsgForm: {
        description: '',
        destination: '',
        log: '',
        ports: '',
        protocol: '',
      },
      editAsgForm: {
        id: '',
        description: '',
        destination: '',
        log: '',
        ports: '',
        protocol: '',
      },
      file: [],
      json: [],
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    initForm() {
      this.addAsgForm.description = '';
      this.addAsgForm.destination = '';
      this.addAsgForm.log = '';
      this.addAsgForm.ports = '';
      this.addAsgForm.protocol = '';
      this.editAsgForm.id = '';
      this.editAsgForm.description = '';
      this.editAsgForm.destination = '';
      this.editAsgForm.log = '';
      this.editAsgForm.ports = '';
      this.editAsgForm.protocol = '';
    },
    getAsgs() {
      const path = 'http://localhost:5000/api/asgs';
      axios.get(path)
        .then((res) => {
          this.asgs = res.data.asgs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addAsg(payload) {
      const path = 'http://localhost:5000/api/add';
      axios.post(path, payload)
        .then(() => {
          this.getAsgs();
          this.message = 'ASG added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getAsgs();
        });
    },
    updateAsg(payload, asgID) {
      const path = `http://localhost:5000/api/asgs/${asgID}`;
      axios.put(path, payload)
        .then(() => {
          this.getAsgs();
          this.message = 'ASG updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAsgs();
        });
    },
    editAsg(asg) {
      this.editAsgForm = asg;
    },
    deleteAsg(asg) {
      this.removeAsg(asg.id);
    },
    removeAsg(asgID) {
      const path = `http://localhost:5000/api/asgs/${asgID}`;
      axios.delete(path)
        .then(() => {
          this.getAsgs();
          this.message = 'ASG removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAsgs();
        });
    },
    generateAsg() {
      const path = 'http://localhost:5000/api/generate-json';
      axios.get(path)
        .then((response) => {
          const data = JSON.stringify(response.data, null, 2);
          const blob = new Blob([data], { type: 'application/json' });
          const link = document.createElement('a');

          link.href = window.URL.createObjectURL(blob);
          link.download = 'asgs.json';
          link.click();
          this.message = 'JSON Generated';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAsgs();
        });
    },
    onSubmitAdd(evt) {
      evt.preventDefault();
      this.$refs.addAsgModal.hide();
      let log = false;
      if (this.addAsgForm.log[0]) log = true;
      const payload = {
        description: this.addAsgForm.description,
        destination: this.addAsgForm.destination,
        log,
        ports: this.addAsgForm.ports,
        protocol: this.addAsgForm.protocol,
      };
      this.addAsg(payload);
    },
    onResetAdd(evt) {
      evt.preventDefault();
      this.$refs.addAsgModal.hide();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editASGModal.hide();
      let log = false;
      if (this.editAsgForm.log[0]) log = true;
      const payload = {
        description: this.editAsgForm.description,
        destination: this.editAsgForm.destination,
        log,
        ports: this.editAsgForm.ports,
        protocol: this.editAsgForm.protocol,
      };
      this.updateAsg(payload, this.editAsgForm.id);
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAsgModal.hide();
      this.getAsgs(); // why?
    },
    handleFileUpload() {
      this.file = this.$refs.file[0];
    },
    onSubmitJson() {
      const path = 'http://localhost:5000/api/upload';
      const formData = new FormData();
      formData.append('file', this.file);
      axios.post(path,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(() => {
          // eslint-disable-next-line
          console.log('SUCCESS!!');
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAsgs();
        });
    },
    onResetJson() {
      this.$refs.file.reset();
    },
  },
  created() {
    this.getAsgs();
  },
};
</script>

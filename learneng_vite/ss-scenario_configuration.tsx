import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import 'jquery/dist/jquery.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'
import styles from './src/customcss/editor.module.css';

const ScenarioConfiguration = () => {
  const [selectedImage, setSelectedImage] = useState<string>('/images/placeholder.png');
  const [formData, setFormData] = useState({
    scenarioID: '',
    level: 1,
    scenarioName: 'scenario_xx',
    scenarioDescription: 'Create a hotel scenario which allow user to book a room',
    characterDescription: 'The ai character will act as a front desk officer in the hotel',
    vocab: 'Reservation, Availability, Occupancy',
  });
  const [isHidden, setIsHidden] = useState(false);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // You can handle form submission here with AJAX or other logic
    console.log(formData);
  };


  let lastScroll = 0;
  const handleScroll = () => {
    const currentScroll = window.pageYOffset || document.documentElement.scrollTop || 0;
    const isScrollingDown = currentScroll > lastScroll;

    if (isScrollingDown) {
      setIsHidden(true);
    } else {
      setIsHidden(false);
    }
    lastScroll = currentScroll;
  };

  React.useEffect(() => {
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  return (
    <div className={styles['editor-body']}>
      <nav className={`${styles['editor-header']} navbar navbar-expand-lg navbar-light px-5 py-2 ${isHidden ? styles.hidden : ''}`}>
        <a className="navbar-brand" href="#">Logo or something</a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
      </nav>

      <div className="d-flex mt-4 justify-content-center pb-3">
        <div className="card col-md-10 border-0 shadow-sm pb-4">
          <div className="card-body mx-2">
            <div className="d-flex justify-content-between border-bottom border-secondary px-1 mb-4 pb-2">
              <h3 className="card-title">Scenario Configuration</h3>
              <button className={`${styles['btn-sc-level']} rounded-pill px-4`} disabled>Level 1</button>
            </div>
            <form
              className="d-flex justify-content-center flex-wrap"
              id="scenarioForm"
              onSubmit={handleSubmit}
            >
              <input type="hidden" name="scenarioID" value={formData.scenarioID} />
              <input type="hidden" name="level" value={formData.level} />
              <div className="scenarioImage mb-4 px-4">
                <div>
                  <img
                    className="rounded mb-3"
                    id="selectedImage"
                    src={selectedImage}
                    alt="Scenario Image"
                    style={{ width: '300px' }}
                  />
                </div>
                <div className="d-flex justify-content-center">
                  <div className={`${styles['btn']} ${styles['btn-primary']} btn btn-primary rounded-pill`} style={{ width: '200px' }}>
                    <label className="form-label m-1" htmlFor="scenarioImage">
                      Choose file
                    </label>
                    <input
                      type="file"
                      className={`${styles['form-control']} form-control d-none`}
                      id="scenarioImage"
                      name="scenarioImage"
                      onChange={handleFileChange}
                    />
                  </div>
                </div>
              </div>
              <div className={`${styles['textfield']} textfield w-100`}>
                <div className="form-group row mb-3">
                  <label className="col-md-3" htmlFor="scenarioName">
                    Name
                  </label>
                  <div className={`${styles['col-md-9']}`}>
                    <input
                      className={`${styles['form-control']} form-control`}
                      type="text"
                      id="scenarioName"
                      name="scenarioName"
                      value={formData.scenarioName}
                      onChange={handleChange}
                    />
                  </div>
                </div>
                <div className="form-group row mb-3">
                  <label className="col-md-3" htmlFor="scenarioDescription">
                    Scenario Description
                  </label>
                  <div className={`${styles['col-md-9']}`}>
                    <textarea
                      className={`${styles['form-control']} form-control`}
                      id="scenarioDescription"
                      rows={5}
                      placeholder="Create a hotel scenario which allows the learner to book a room."
                      name="scenarioDescription"
                      value={formData.scenarioDescription}
                      onChange={handleChange}
                    />
                  </div>
                </div>
                <div className="form-group row mb-3">
                  <label className="col-md-3" htmlFor="characterDescription">
                    Character Description
                  </label>
                  <div className={`${styles['col-md-9']} input-group`}>
                    <textarea
                      className={`rounded-0 rounded-top ${styles['form-control']} form-control w-100`}
                      id="characterDescription"
                      rows={5}
                      placeholder="The ai character will act as a front desk officer in the hotel."
                      name="characterDescription"
                      value={formData.characterDescription}
                      onChange={handleChange}
                    />
                    <button type="button" className={`form-button ${styles['btn-conf-character']} ${styles['btn-primary']} btn-primary border-0 rounded-0 rounded-bottom w-100 py-2`}>
                      <i className="bi-gear me-2"></i>Character Configuration
                    </button>
                  </div>
                </div>
                <div className="form-group row mb-3">
                  <label className="col-md-3" htmlFor="vocab">
                    Vocabularies
                  </label>
                  <div className={`${styles['col-md-9']}`}>
                    <textarea
                      className={`${styles['form-control']} form-control`}
                      id="vocab"
                      rows={2}
                      placeholder="Reservation, Availability, Occupancy"
                      name="vocab"
                      value={formData.vocab}
                      onChange={handleChange}
                    />
                  </div>
                </div>
              </div>

              <div className="d-flex justify-content-end w-100">
                <button type="button" className={`${styles['btn']} btn px-5 link rounded-pill`}>
                  Cancel
                </button>
                <button type="submit" className={`${styles['btn']} ${styles['btn-primary']} btn-primary px-5 rounded-pill`}>
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScenarioConfiguration;


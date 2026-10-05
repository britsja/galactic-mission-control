const characterInput = document.querySelector('#character-id');
const searchButton = document.querySelector('#character-search');
const randomButton = document.querySelector('#random-character');
const characterResult = document.querySelector('#character-result');
const missionForm = document.querySelector("#mission-form");
const missionResult = document.querySelector("#mission-result");

async function getCharacter(characterId) {
  characterResult.innerHTML = `
    <p class="placeholder">
      Retreiving galactic intelligence...
    </p>
  `;

  try {
    const response = await fetch(
      `/api/v1/characters/${characterId}`
    )

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.error || "Unable to retreive character"
      );
    }

    displayCharacter(data);
  } catch(error) {
    characterResult.innerHTML = `
      <p class="error">${error.message}</p>
    `;
  }
}

function displayCharacter(character) {
  characterResult.innerHTML = `
    <h3 class="character-name">
      ${character.name}
    </h3>

    <div class="data-row">
      <span class="data-label">Character ID</span>
      <span class="data-value">
        ${character.character_id}
      </span>
    </div>

    <div class="data-row">
      <span class="data-label">Birth Year</span>
      <span class="data-value">
        ${character.birth_year}
      </span>
    </div>

    <div class="data-row">
      <span class="data-label">Height</span>
      <span class="data-value">
        ${character.height} cm
      </span>
    </div>

    <div class="data-row">
      <span class="data-label">Mass</span>
      <span class="data-value">
        ${character.mass} kg
      </span>
    </div>

    <div class="data-row">
      <span class="data-label">Eye Color</span>
      <span class="data-value">
        ${character.profile.eye_color}
      </span>
    </div>

    <div class="data-row">
      <span class="data-label">Gender</span>
      <span class="data-value">
        ${character.profile.gender}
      </span>
    </div>
  `;
}

missionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const missionName = document.querySelector("#mission-name").value;
  const characterIdsInput = document.querySelector("#character-ids").value;
  const planetId = document.querySelector("#planet-id").value;
  
  const characterIds = characterIdsInput
    .split(",")
    .map(id => Number(id.trim()))
    .filter(id => !Number.isNaN(id));


  const missionData = {
    mission_name: missionName,
    character_ids: characterIds,
    planet_id: Number(planetId),
  };

  missionResult.innerHTML = `
    <p class="placeholder">
      Assembling mission...
    </p>
  `;

  try {
    const response = await fetch(
      "/api/v1/missions",
      {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(missionData),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.error || "Mission creation failed"
      );
    }

    displayMission(data);

  } catch (error) {
    missionResult.innerHTML = `
      <p class="error">${error.message}</p>
    `;
  }
});

searchButton.addEventListener("click", () => {
  const characterId = characterInput.value;
  if (!characterId) {
    return;
  }
  getCharacter(characterId);
});

randomButton.addEventListener("click", () => {
  const randomId = Math.floor(Math.random() * 83) + 1;
  characterInput.value = randomId;
  getCharacter(randomId);
})


function displayMission(mission) {
  const crewHtml = mission.crew
    .map(character => `
      <li>
        ${character.name}
        <span class="data-label">
          #${character.character_id}
        </span>
      </li>
    `)
    .join("");


  missionResult.innerHTML = `
    <span class="mission-status">
      ${mission.status}
    </span>
    <h3>
      ${mission.mission_name}
    </h3>
    <div class="data-row">
      <span class="data-label">
          Destination
      </span>
      <span class="data-value">
          ${mission.destination}
      </span>
    </div>
    <div class="data-row">
      <span class="data-label">
          Crew Size
      </span>
      <span class="data-value">
          ${mission.crew_size}
      </span>
    </div>
    <h4>Assigned Crew</h4>
    <ul class="crew-list">
      ${crewHtml}
    </ul>
  `;
}
import React, { useState, useEffect, useMemo } from "react";
import 'bootstrap/dist/css/bootstrap.css';
import 'jquery/dist/jquery.min.js'
import styles from './customcss/chatting.module.css';
import { Experience } from "@/components/Experience";
import { Canvas } from "@react-three/fiber";

const Chatting = () => {

    const [backImage, setBackImage] = useState < string > ('/images/back.png');
    const [userImage, setUserImage] = useState < string > ('/images/user.png');
    const [homeImage, setHomeImage] = useState < string > ('/images/home.png');

    return (
        <div className={styles['chatting-body']}>
            <div className={styles['header']}>
                <div className={styles['icons']}>
                    <a href="level_page.html">
                        <img src={backImage} alt="Back" />
                    </a>
                    <div className={styles["level-indicator"]}>Easy</div>
                </div>
                <div className={styles['title']}>Scenario 1 - Booking Room</div>
                <div className={styles['icons']}>
                    <img src={homeImage} alt="Home" />
                    <img src={userImage} alt="Profile" />
                </div>
            </div>

            <div className={styles['main-container']}>
                <div className={styles["left-panel"]}>
                    <Canvas shadows camera={{ position: [0, 0, 8], fov: 7 }}>
                        <Experience />
                    </Canvas>
                    <div className={styles["ai-name"]}>Joseph</div>
                    <div className={styles["ai-description"]}>Description</div>
                </div>

                <div className={styles['right-panel']}>
                    <div className={styles["chat-area"]} id="chatArea"></div>

                    <div className={styles['summary-btn-alignment']}>
                        <a href="summary.html" className={styles["summary-btn"]}>Summary</a>
                    </div>
                </div>
            </div>
        </div>
    );
}
export default Chatting;
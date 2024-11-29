import React, { useState } from "react";
import 'bootstrap/dist/css/bootstrap.css';
import Col from 'react-bootstrap/Col';
import Nav from 'react-bootstrap/Nav';
import Row from 'react-bootstrap/Row';
import Tab from 'react-bootstrap/Tab';
import styles from './customcss/editor.module.css';

const testing = () => {
    const [activeKey, setActiveKey] = useState<string | null>("first");

    const handleSelect = (selectedKey: string | null) => {
        setActiveKey(selectedKey);
    };

    const isActive = (key: string) => activeKey === key;

    return (
        <Tab.Container id="left-tabs-example" defaultActiveKey="first">
            <Row>
                <Col>
                    <Nav variant="pills" className="flex-column" onSelect={handleSelect}>
                        <Nav.Item>
                            <Nav.Link eventKey="first" className={`${isActive("first") ? styles.tabIsActive : styles.tabNotActive}`}>Tab 1</Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="second" className={`${isActive("second") ? styles.tabIsActive : styles.tabNotActive}`}>Tab 2</Nav.Link>
                        </Nav.Item>
                    </Nav>
                </Col>
                <Col sm={9}>
                    <Tab.Content>
                        <Tab.Pane eventKey="first">First tab content</Tab.Pane>
                        <Tab.Pane eventKey="second">Second tab content</Tab.Pane>
                    </Tab.Content>
                </Col>
            </Row>
        </Tab.Container>
    );
};

export default testing;
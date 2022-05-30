import React, { useState } from 'react';
import './uploadPDF.css';
import axios from 'axios';
import { Col, Container, Row, Dropdown, Button, Modal } from 'react-bootstrap';
import page1 from './images/output_000.jpg';
import page2 from './images/output_001.jpg';
import page3 from './images/output_001.jpg';
import page4 from './images/output_001.jpg';

class UploadPDF extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            selectedPDF: null,
            fullPath: null
        }
    }
    sendPDFtoBackend() {
        console.log("Send PDF to BACK");
        console.log(this.state.fullPath);

        // const bodyFormData = JSON.stringify({
        //     "file": this.state.selectedPDF,
        //     "text": "C:\\work_of_tuteck\\PDF_OCR_Fraud_Detection\\ocr-fraud-detection-back\\Dinesh\\SBI statement.pdf",
        // });


        var bodyFormData = new FormData();
        bodyFormData.append('file', this.state.selectedPDF);
        bodyFormData.append('text', 'C:\\work_of_tuteck\\PDF_OCR_Fraud_Detection\\ocr-fraud-detection-back\\Dinesh\\SBI statement.pdf');
        axios({
            method: "post",
            url: "http://192.168.0.173:4000/predict",
            data: bodyFormData,
            headers: { "Content-Type": "multipart/form-data" },
        })
            .then((resData) => {
                console.log(resData.data);
                this.setState({
                    resData: resData.data
                })
            })
            .catch((err) => {
                console.log("ERROR==>>", err);
            })
    }

    render() {

        return (
            <>

                <input type={"file"} accept="pdf" className='uploadArea'
                    onChange={(e) => this.setState({ selectedPDF: e.target.files[0], fullPath: e.target.files[0].mozFullPath })}></input>
                <div className='uploadBtn' onClick={() => { this.sendPDFtoBackend() }}>Upload Transaction File</div>



                <div className='afterDetection'>
                    <div className="row">
                        <h1>After Detection</h1><br />
                    </div>
                    <div className="row">
                        <div className="col-sm-6">
                            <img src={page1} className="image-style"></img>
                            <img src={page2} className="image-style"></img>
                            <img src={page3} className="image-style"></img>
                            <img src={page4} className="image-style"></img>
                        </div>
                        <div className="col-sm-6">
                            <img src={page1} className="image-style"></img>
                            <img src={page2} className="image-style"></img>
                            <img src={page3} className="image-style"></img>
                            <img src={page4} className="image-style"></img>
                        </div>
                    </div>
                </div>
            </>
        )
    }
}

export default UploadPDF
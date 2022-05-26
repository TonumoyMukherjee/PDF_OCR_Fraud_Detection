import React, { useState } from 'react';
import './uploadPDF.css';
import axios from 'axios';
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
            url: "http://127.0.0.1:5000/predict",
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
                <input type={"file"} accept="pdf"
                    onChange={(e) => this.setState({ selectedPDF: e.target.files[0], fullPath: e.target.files[0].mozFullPath })}></input>
                <div className='uploadBtn' onClick={() => { this.sendPDFtoBackend() }}>Upload Transaction File</div>

                <p>
                    {this.state.resData}
                </p>
            </>
        )
    }
}

export default UploadPDF
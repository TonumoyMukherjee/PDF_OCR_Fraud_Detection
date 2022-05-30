import React, { useState } from 'react';
import './uploadPDF.css';
import axios from 'axios';
import { Col, Container, Row, Dropdown, Button, Modal } from 'react-bootstrap';

class UploadPDF extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            selectedPDF: null,
            fullPath: null,
            IsResponseRecieved: false,
            IsUploadClicked: false,
        }
        this.totalPage = 31;
        this.pages = [];
        this.highlightpages = [];
        for (let i = 0; i <= this.totalPage; i++) {
            if (i < 10) {
                this.pages.push("output_00" + i + ".jpg");
                this.highlightpages.push("output_00" + i + ".jpg");
            }
            else {
                this.pages.push("output_0" + i + ".jpg");
                this.highlightpages.push("output_0" + i + ".jpg");
            }

        }
        console.log(this.pages);
    }
    sendPDFtoBackend() {

        this.setState({
            IsUploadClicked: true
        })
        // console.log("Send PDF to BACK");
        // console.log(this.state.fullPath);

        // const bodyFormData = JSON.stringify({
        //     "file": this.state.selectedPDF,
        //     "text": "C:\\work_of_tuteck\\PDF_OCR_Fraud_Detection\\ocr-fraud-detection-back\\Dinesh\\SBI statement.pdf",
        // });


        var bodyFormData = new FormData();
        // bodyFormData.append('file', this.state.selectedPDF);
        bodyFormData.append('text', 'AXIS_statement.pdf');
        axios({
            method: "post",
            url: "http://127.0.0.1:5000/predict",
            data: bodyFormData,
            headers: { "Content-Type": "multipart/form-data" },
        })
            .then((resData) => {
                console.log(resData.data);
                this.setState({
                    IsResponseRecieved: true
                })
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
                {
                    !this.state.IsResponseRecieved ?
                        <>
                            <input type={"file"} accept="pdf" className='uploadArea'
                                onChange={(e) => this.setState({ selectedPDF: e.target.files[0], fullPath: e.target.files[0].mozFullPath })}></input>
                            <div className='uploadBtn' onClick={() => { this.sendPDFtoBackend() }}>Upload Transaction File</div>
                        </>
                        :
                        <></>
                }




                {this.state.IsResponseRecieved ?
                    <>
                        <div className='afterDetection'>
                            <div className="row">
                                <h1>After Detection</h1><br />
                            </div>
                            <div className="row">
                                <div className="col-sm-6">

                                    {this.pages?.map((image_name) => (
                                        <img src={"http://127.0.0.1:5000/getfile/" + image_name} className='image-style' />
                                    ))}
                                </div>
                                {this.highlightpages?.map((image_name) => (
                                    <img src={"http://127.0.0.1:5000/gethighlightedfile/" + image_name} className='image-style' />
                                ))}
                            </div>
                        </div>
                    </>
                    : <>
                        {
                            this.state.IsUploadClicked ?
                                <div className='loadingstyle'>Processing..</div> :
                                <></>
                        }

                    </>
                }

            </>
        )
    }
}

export default UploadPDF
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
            totalPage: '',
            beforeImages: [],
            afterImages: []
        }
    }

    makePages(totalPage) {
        let pages = [];
        let highlightpages = [];
        for (let i = 0; i <= totalPage; i++) {
            if (i < 10) {
                pages.push("output_00" + i + ".jpg");
                highlightpages.push("output_00" + i + ".jpg");
            }
            else {
                pages.push("output_0" + i + ".jpg");
                highlightpages.push("output_0" + i + ".jpg");
            }
        }
        this.setState({
            beforeImages: pages,
            afterImages: highlightpages
        })
        // console.log(pages)
        // console.log(highlightpages)
    }

    sendPDFtoBackend() {

        this.setState({
            IsUploadClicked: true
        })

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
                let number_of_pages = JSON.parse(resData.data.replaceAll('NaN', '0')).number_of_pages;

                this.setState({
                    IsResponseRecieved: true,
                    resData: JSON.parse(resData.data.replaceAll('NaN', '0')),
                    totalPage: number_of_pages
                })
                this.makePages(number_of_pages);
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
                                <div className="col-sm-6"><h1>Before</h1></div>
                                <div className="col-sm-6"><h1>After</h1></div>
                            </div>
                            <div className="row">
                                <div className="col-sm-6">

                                    {this.state.beforeImages?.map((image_name) => (
                                        <img src={"http://127.0.0.1:5000/getfile/" + image_name} className='image-style' />
                                    ))}
                                </div>
                                {this.state.afterImages?.map((image_name) => (
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
import React, { useState } from 'react';
import UploadPDF from '../uploadPDF/uploadPDF';
import DisplayPDF from '../displayPDF/displayPDF';
import './HomePage.css';

class HomePage extends React.Component {
    constructor(props) {
        super(props);
    }
    render() {

        return (
            <>
                <p className='HomePageHeadingText'>OCR Fraud Detection POC</p>
                <UploadPDF />
                <br />
                <DisplayPDF />
            </>
        )
    }
}

export default HomePage
import { useState } from 'react'
import { Button, Modal } from 'react-bootstrap'

const FormModel = ({ edit = false, title, onSubmit, children }) => {
  const [show, setShow] = useState(false)

  const handleClose = () => setShow(false)
  const handleShow = () => setShow(true)

  const handleSubmit = async (e) => {
    e.preventDefault()
    const success = await onSubmit()
    if (success) {
      setShow(false);
    }
  }

  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        {edit ? 'Edit' : 'New'}
      </Button>

      <Modal show={show} onHide={handleClose} size='lg' aria-labelledby="contained-modal-title-vcenter" centered>
        <Modal.Header closeButton>
          <Modal.Title>{edit ? 'Edit ' : 'New '}{title}</Modal.Title>
        </Modal.Header>
        <form onSubmit={handleSubmit}>
          <Modal.Body>
            {children}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Close
            </Button>
            <Button variant="primary" type='submit'>
              {edit ? 'Update' : 'Save'}
            </Button>
          </Modal.Footer>
        </form>
      </Modal>
    </>
  );
}

export default FormModel
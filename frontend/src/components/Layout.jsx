import { useState, forwardRef } from 'react';
import {
	Container,
	Navbar,
	Dropdown,
	ListGroup,
	Row,
	Col,
	Breadcrumb
} from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';
import { Link, useLocation } from 'react-router-dom';

const Layout = ({ children }) => {
	const { user } = useAuth()
	const location = useLocation();
	const pathnames = location.pathname.split('/').filter(Boolean);
	const [activeLink, setActiveLink] = useState('/')

	const links = [
		{ url: '/', name: 'Dashboard' },
	]

	return (
		<div>
			<Navbar className="bg-body-tertiary" sticky='top'>
				<Container>
					<Navbar.Brand as={Link} to='/'>Auth App</Navbar.Brand>
					<Navbar.Toggle />
					<Navbar.Collapse className="justify-content-end">
						<Navbar.Text>
							<div className='d-flex justify-content-center gap-2'>
								<div>Hi!</div>
								<Dropdown align="start" drop='start'>
									<Dropdown.Toggle as={CustomToggle} className='bg-primary rounded-circle'>
										{user.username}
									</Dropdown.Toggle>

									<Dropdown.Menu>
										<Dropdown.Item as={Link} to='/edit-profile'>Edit Profile</Dropdown.Item>
										<Dropdown.Item as={Link} to='/change-password'>Change Password</Dropdown.Item>
										<Dropdown.Divider />
										<Dropdown.Item as={Link} to='/logout'>Logout</Dropdown.Item>
									</Dropdown.Menu>
								</Dropdown>
							</div>
						</Navbar.Text>
					</Navbar.Collapse>
				</Container>
			</Navbar>

			<Row>
				<Col md={2} sm={12}>
					<ListGroup as="ul" className='sidebar'>
						{
							links.map((link, index) => (
								<Link to={link.url} key={index}>
									<ListGroup.Item as="li" active={activeLink == link.url}>
										{link.name}
									</ListGroup.Item>
								</Link>
							))
						}
					</ListGroup>
				</Col>
				<Col md={10} sm={12} className='p-4'>
					<Breadcrumb className='mb-4'>
						<Breadcrumb.Item linkAs={Link} linkProps={{ to: '/' }}>
							Home
						</Breadcrumb.Item>

						{
							pathnames.map((value, index) => {
								const to = `/${pathnames.slice(0, index + 1).join('/')}`;
								const isLast = index === pathnames.length - 1;

								return isLast ? (
									<Breadcrumb.Item active key={to}>{value}</Breadcrumb.Item>
								) : (
									<Breadcrumb.Item linkAs={Link} linkProps={{ to }} key={to}>
										{decodeURIComponent(value)}
									</Breadcrumb.Item>
								);
							})
						}
					</Breadcrumb>
					{children}
				</Col>
			</Row>

		</div>
	)
}

export default Layout

const CustomToggle = forwardRef(({ children, onClick }, ref) => (
	<Link
		to=""
		ref={ref}
		onClick={(e) => {
			e.preventDefault();
			onClick(e);
		}}
	>
		{children}
	</Link>
));